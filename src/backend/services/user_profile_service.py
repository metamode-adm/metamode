import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.core.templates import templates
from src.backend.core.messages import (
    USER_EMAIL_ALREADY_EXISTS,
    USER_PASSWORD_WEAK,
    USER_UPDATE_SUCCESS,
    NO_PERMISSION_MSG
)
from src.backend.core.responses import json_response
from src.backend.services.auth_service import hash_password, is_password_strong
from src.backend.services.permission_service import check_permission
from src.backend.repositories.user_repository import get_user_by_email, update_user_db
from src.backend.repositories.slideshow_repository import get_slideshows_shared_with_user
from src.backend.validators.user_validator import is_email_already_used
from src.backend.models.user_model import User 
from fastapi.responses import RedirectResponse
from fastapi import status
from src.backend.core.responses import set_flash_message
from fastapi import Request
logger = logging.getLogger(__name__)


async def render_profile_page(request: Request, session: AsyncSession, user: User):
    """
    Renderiza a página de perfil do usuário logado com seus dados e slideshows compartilhados.
    """

    has_permission = await check_permission(user, "can_edit_own_profile")
    if not has_permission:
        set_flash_message(request, NO_PERMISSION_MSG)
        return RedirectResponse(url="/no-permission", status_code=status.HTTP_303_SEE_OTHER)
        

    flash_message = request.session.pop("flash_message", None)

    slideshows = await get_slideshows_shared_with_user(session, user.id)

    shared_slides = [
        {
            "id": s.id,
            "title": s.title,
            "description": s.description,
            "cover_path": s.cover.filepath if s.cover else None,
            "media_count": len(s.media_files),
            "user_count": len(s.access_list),
        }
        for s in slideshows
    ]

    context = {
        "request": request,
        "user_data": user,  
        "slideshows": shared_slides,
        "user": user,  
        "flash_message": flash_message  
    }

    logger.info(f"Perfil carregado para o usuário: {user.username}")
    return templates.TemplateResponse("user/profile.html", context)


async def update_profile_data(data, session: AsyncSession, user: User):
    """
    Atualiza o nome de usuário e email do próprio usuário.
    """
    has_permission = await check_permission(user, "can_edit_own_profile")
    if not has_permission:
        return json_response(success=False, message=NO_PERMISSION_MSG, status_code=403)


    user = await get_user_by_email(session, user.email)
    updated = False

    if data.username and data.username != user.username:
        user.username = data.username
        updated = True

    if data.email and data.email != user.email:
        if await is_email_already_used(session, data.email, exclude_user_id=user.id):
            return json_response(False, USER_EMAIL_ALREADY_EXISTS)
        user.email = data.email
        updated = True

    if updated:
        await update_user_db(session, user)
        logger.info(f"Usuário {user.username} atualizou seu perfil com sucesso.")

    return json_response(True, USER_UPDATE_SUCCESS)


async def update_profile_password(data, session: AsyncSession, user: User):
    """
    Atualiza a senha do usuário logado.
    """
    has_permission = await check_permission(user, "can_edit_own_profile")
    if not has_permission:
        return json_response(success=False, message=NO_PERMISSION_MSG, status_code=403)

    if not is_password_strong(data.new_password):
        return json_response(False, USER_PASSWORD_WEAK)

    user = await get_user_by_email(session, user.email)
    user.hashed_password = hash_password(data.new_password)
    await update_user_db(session, user)

    logger.info(f"Senha atualizada com sucesso para o usuário: {user.username}")
    return json_response(True, USER_UPDATE_SUCCESS)
