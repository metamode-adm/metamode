import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from src.backend.models.slideshow_model import Slideshow
from src.backend.models.user_model import User
from src.backend.models.user_slideshow_access_model import UserSlideshowAccess
from src.backend.core.responses import json_response
from src.backend.core.messages import (
    SLIDESHOW_NOT_FOUND,
    USER_NOT_FOUND,
    USER_ALREADY_EXISTS,
    USER_DELETE_SUCCESS,
    USER_UPDATE_ERROR,
    ACCESS_USER_ADDED_SUCCESS,
    SUCCESS_OPERATION,
    NO_PERMISSION_MSG
)
from src.backend.services.permission_service import check_permission  # <- Aqui!

logger = logging.getLogger(__name__)


async def get_slideshow_access_info(slideshow_id: int, session: AsyncSession, user):
    """Retorna os dados de acesso (usuários) vinculados à pasta."""
    
    has_permission = await check_permission(user, "can_view_sharing")
    if not has_permission:
        return json_response(success=False, message=NO_PERMISSION_MSG, status_code=403)


    result = await session.execute(
        select(Slideshow)
        .where(Slideshow.id == slideshow_id)
        .options(selectinload(Slideshow.access_list).joinedload(UserSlideshowAccess.user))
    )

    slideshow = result.scalars().first()

    if not slideshow:
        raise HTTPException(status_code=404, detail=SLIDESHOW_NOT_FOUND)

    users = [
        {
            "id": access.user.id,
            "name": access.user.username,
            "email": access.user.email,
        }
        for access in slideshow.access_list
    ]

    return json_response(
        success=True,
        message=SUCCESS_OPERATION,
        data={
            "title": slideshow.title,
            "description": slideshow.description,
            "access": users,
        }
    )


async def add_user_to_slideshow_access(slideshow_id: int, data: dict, session: AsyncSession, user):
    """Adiciona um usuário à pasta (slideshow) com permissão de acesso."""

    has_permission = await check_permission(user, "can_add_users_to_slideshow")
    if not has_permission:
        return json_response(success=False, message=NO_PERMISSION_MSG, status_code=403)


    try:
        user_id = data.get("user_id")
        can_edit = data.get("can_edit", False)

        slideshow = await session.get(Slideshow, slideshow_id)
        if not slideshow:
            return json_response(success=False, message=SLIDESHOW_NOT_FOUND, status_code=404)

        user_target = await session.get(User, user_id)
        if not user_target:
            return json_response(success=False, message=USER_NOT_FOUND, status_code=404)

        result = await session.execute(
            select(UserSlideshowAccess).where(
                UserSlideshowAccess.user_id == user_id,
                UserSlideshowAccess.slideshow_id == slideshow_id
            )
        )
        if result.scalar():
            return json_response(success=False, message=USER_ALREADY_EXISTS, status_code=400)

        access = UserSlideshowAccess(
            user_id=user_id,
            slideshow_id=slideshow_id,
            can_edit=can_edit
        )
        session.add(access)
        await session.commit()

        return json_response(success=True, message=ACCESS_USER_ADDED_SUCCESS)

    except Exception as e:
        await session.rollback()
        logger.error(f"Erro ao adicionar usuário à pasta: {e}")
        return json_response(success=False, message=USER_UPDATE_ERROR, status_code=500)


async def remove_user_from_slideshow_access(slideshow_id: int, user_id: str, session: AsyncSession, user):
    """Remove o vínculo de acesso de um usuário à pasta (slideshow)."""

    has_permission = await check_permission(user, "can_share_slideshow")
    if not has_permission:
        return json_response(success=False, message=NO_PERMISSION_MSG, status_code=403)


    try:
        result = await session.execute(
            select(UserSlideshowAccess).where(
                UserSlideshowAccess.user_id == user_id,
                UserSlideshowAccess.slideshow_id == slideshow_id
            )
        )
        access = result.scalar_one_or_none()
        if not access:
            return json_response(success=False, message=USER_NOT_FOUND, status_code=404)

        await session.delete(access)
        await session.commit()

        return json_response(success=True, message=USER_DELETE_SUCCESS)

    except Exception as e:
        await session.rollback()
        logger.error(f"Erro ao remover acesso: {e}")
        return json_response(success=False, message=USER_UPDATE_ERROR, status_code=500)


async def search_users_for_slideshow(q: str, slideshow_id: int, session: AsyncSession, user):
    """Busca usuários pelo nome ou e-mail que ainda não possuem acesso à pasta."""

    has_permission = await check_permission(user, "can_search_users")
    if not has_permission:
        return json_response(success=False, message=NO_PERMISSION_MSG, status_code=403)

    try:
        subquery = select(UserSlideshowAccess.user_id).where(
            UserSlideshowAccess.slideshow_id == slideshow_id
        ).subquery()

        result = await session.execute(
            select(User.id, User.username, User.email)
            .where(
                (User.username.ilike(f"%{q}%")) | (User.email.ilike(f"%{q}%")),
                User.id.notin_(subquery),
                User.is_active == True
            )
            .limit(10)
        )

        users = [
            {"id": row.id, "username": row.username, "email": row.email}
            for row in result.fetchall()
        ]

        return json_response(success=True, message=SUCCESS_OPERATION, data=users)

    except Exception as e:
        logger.error(f"Erro ao buscar usuários: {e}")
        return json_response(success=False, message=USER_UPDATE_ERROR, status_code=500)


async def get_user_slideshows(user_id: str, session: AsyncSession, user):
    """Retorna todas as pastas (slideshows) às quais o usuário tem acesso."""

    has_permission = await check_permission(user, "can_view_user_slideshows")
    if not has_permission:
        return json_response(success=False, message=NO_PERMISSION_MSG, status_code=403)


    result = await session.execute(
        select(Slideshow)
        .join(UserSlideshowAccess)
        .where(UserSlideshowAccess.user_id == user_id)
    )
    slideshows = result.scalars().all()

    return json_response(
        success=True,
        message=SUCCESS_OPERATION,
        data=[
            {
                "id": s.id,
                "title": s.title,
                "description": s.description
            }
            for s in slideshows
        ]
    )
