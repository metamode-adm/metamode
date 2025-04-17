import logging
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.repositories.user_repository import (
    get_all_users_db,
    get_user_by_id,
    get_user_by_email,
    get_user_by_username,
    get_role_by_name,
    create_user_db,
    delete_user_db,
    update_user_db,
)

from fastapi.responses import RedirectResponse
from fastapi import status
from src.backend.core.responses import set_flash_message
from src.backend.services.auth_service import hash_password, is_password_strong
from src.backend.services.permission_service import check_permission
from src.backend.validators.user_validator import is_email_already_used
from src.backend.models.user_model import User
from src.backend.core.messages import (
    USER_ALREADY_EXISTS,
    USER_CREATE_SUCCESS,
    USER_DELETE_SUCCESS,
    USER_EMAIL_ALREADY_EXISTS,
    USER_NOT_FOUND,
    USER_PASSWORD_WEAK,
    USER_UPDATE_SUCCESS,
    NO_PERMISSION_MSG
)
from src.backend.core.responses import json_response
from src.backend.core.base_view import render_admin_template

logger = logging.getLogger(__name__)


async def list_all_users(request, session: AsyncSession, user: User):
    """Renderiza a página com todos os usuários cadastrados."""

    has_permission = await check_permission(user, "can_create_user")
    if not has_permission:
        set_flash_message(request, NO_PERMISSION_MSG)
        return RedirectResponse(url="/no-permission", status_code=status.HTTP_303_SEE_OTHER)

    users = await get_all_users_db(session)

    user_list = [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "is_active": bool(u.is_active),
            "created_at": u.created_at.strftime("%d/%m/%Y %H:%M"),
            "role": u.role if u.role else "Sem função",
        }
        for u in users
    ]

    # Ordena alfabeticamente pelo username (case insensitive)
    user_list = sorted(user_list, key=lambda x: x["username"].lower())

    logger.info(f"Listagem de usuários solicitada por {user.username}")
    return await render_admin_template(
        request,
        "admin/user_management.html",
        {"users": user_list, "current_user": user},
        user=user,
    )

async def create_new_user(user_data, session: AsyncSession, user: User):
    """Cria um novo usuário com validações de e-mail, permissões e senha."""

    has_permission = await check_permission(user, "can_create_user")
    if not has_permission:
        return json_response(success=False, message=NO_PERMISSION_MSG, status_code=403)

    if await is_email_already_used(session, user_data.email):
        return json_response(False, USER_EMAIL_ALREADY_EXISTS)

    if await get_user_by_username(session, user_data.username):
        return json_response(False, USER_ALREADY_EXISTS)

    if user_data.role == "superadmin":
        await check_permission(user, "can_create_superadmin")

    role = await get_role_by_name(session, user_data.role)
    if not role:
        return json_response(False, f"Função '{user_data.role}' não encontrada.")

    hashed_password = hash_password(user_data.password)

    user = await create_user_db(
        session=session,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=user_data.is_active,
        role_name=role.name,
    )

    logger.info(f"Usuário criado com sucesso: {user.username}")
    return json_response(True, USER_CREATE_SUCCESS)


async def delete_user(user_id: str, session: AsyncSession, user: User):
    """Remove um usuário do sistema com base nas permissões do solicitante."""

    has_permission = await check_permission(user, "can_remove_user")
    if not has_permission:
        return json_response(success=False, message=NO_PERMISSION_MSG, status_code=403)

    user = await get_user_by_id(session, user_id)
    if not user:
        return json_response(False, USER_NOT_FOUND)

    if user.role and user.role.name == "superadmin":
        await check_permission(user, "can_remove_admins")

    await delete_user_db(session, user)
    logger.info(f"Usuário removido: {user.username}")
    return json_response(True, USER_DELETE_SUCCESS)


async def update_user_data(user_id: str, user_data, session: AsyncSession, user: User):
    """Atualiza os dados de um usuário com validações de permissão e unicidade."""

    has_permission = await check_permission(user, "can_edit_roles")
    if not has_permission:
        return json_response(success=False, message=NO_PERMISSION_MSG, status_code=403)

    user = await get_user_by_id(session, user_id)
    if not user:
        return json_response(False, USER_NOT_FOUND)

    if user_data.username and user_data.username != user.username:
        if await get_user_by_username(session, user_data.username):
            return json_response(False, USER_ALREADY_EXISTS)
        user.username = user_data.username

    if user_data.email and user_data.email != user.email:
        if await is_email_already_used(session, user_data.email, exclude_user_id=user_id):
            return json_response(False, USER_EMAIL_ALREADY_EXISTS)
        user.email = user_data.email

    if user_data.password:
        if not is_password_strong(user_data.password):
            return json_response(False, USER_PASSWORD_WEAK)
        user.hashed_password = hash_password(user_data.password)

    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    if user_data.role:
        role = await get_role_by_name(session, user_data.role)
        if not role:
            return json_response(False, f"Função '{user_data.role}' não encontrada.")
        if role.name == "superadmin":
            await check_permission(user, "can_create_superadmin")
        user.role = role

    await update_user_db(session, user)
    logger.info(f"Usuário atualizado: {user.username}")
    return json_response(True, USER_UPDATE_SUCCESS)
