import logging
from fastapi import Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.backend.core.responses import set_flash_message
from src.backend.core.responses import json_response
from src.backend.core.config import settings
from src.backend.core.base_view import render_admin_template
from src.backend.core.messages import (
    SLIDESHOW_CREATED_SUCCESS,
    SLIDESHOW_CREATION_FAILED,
    SLIDESHOW_NOT_FOUND,
    SLIDESHOW_NAME_DUPLICATE,
    SLIDESHOW_REQUIRED_FIELDS,
    SUCCESS_OPERATION,
    NO_PERMISSION_MSG
)

from fastapi.responses import RedirectResponse

from src.backend.schemas.slideshow_schema import SlideshowCreateSchema, SlideshowUpdateSchema
from src.backend.storage.media_storage import delete_file
from src.backend.repositories.slideshow_repository import (
    get_all_slideshows_with_cover,
    get_slideshow_with_media,
    get_slideshow_by_id,
    create_slideshow_db,
    get_media_ids_by_slideshow,
    update_media_order,
    get_all_medias,
    get_medias_by_slideshow_id,
    delete_slideshow_and_related
)
from src.backend.services.permission_service import check_permission

logger = logging.getLogger(__name__)


from fastapi import HTTPException, status

async def list_slideshows(request: Request, session: AsyncSession, user):
    """Lista todos os slideshows disponíveis."""
    has_permission = await check_permission(user, "can_view_slideshow")
    if not has_permission:
        return RedirectResponse(url="/profile", status_code=status.HTTP_303_SEE_OTHER)

    slideshows = await get_all_slideshows_with_cover(session)
    for slideshow in slideshows:
        if slideshow.cover and not slideshow.cover.filepath.startswith("/"):
            slideshow.cover.filepath = f"/{settings.UPLOAD_DIR}/{slideshow.cover.filepath}"

    return await render_admin_template(
        request,
        "admin/slideshow_list.html",
        {"slideshows": slideshows},
        user=user
    )


async def create_slideshow(data: SlideshowCreateSchema, session: AsyncSession, user):
    """Cria uma nova pasta (slideshow) com título e identificador únicos."""
    has_permission = await check_permission(user, "can_create_slideshow")
    if not has_permission:
        return json_response(success=False, message=NO_PERMISSION_MSG, status_code=403)
    
    try:
        name = data.name or SlideshowCreateSchema.generate_slug_from_title(data.title)

        if not name.isidentifier():
            return json_response(success=False, message=SLIDESHOW_REQUIRED_FIELDS, status_code=400)

        data.name = name
        await create_slideshow_db(data, session)

        return json_response(success=True, message=SLIDESHOW_CREATED_SUCCESS)

    except IntegrityError as e:
        await session.rollback()
        if "Duplicate entry" in str(e.orig):
            return json_response(success=False, message=SLIDESHOW_NAME_DUPLICATE, status_code=400)
        logger.error(f"Erro de integridade ao criar slideshow: {e}")
        return json_response(success=False, message=SLIDESHOW_CREATION_FAILED, status_code=500)

    except Exception as e:
        await session.rollback()
        logger.error(f"Erro inesperado ao criar slideshow: {e}")
        return json_response(success=False, message=SLIDESHOW_CREATION_FAILED, status_code=500)


async def view_slideshow(slideshow_id: int, request: Request, session: AsyncSession, user):
    """Exibe todas as mídias dentro de um slideshow específico."""

    has_permission = await check_permission(user, "can_view_media")
    if not has_permission:
        set_flash_message(request, NO_PERMISSION_MSG)
        return RedirectResponse(url="/no-permission", status_code=status.HTTP_303_SEE_OTHER)

    slideshow = await get_slideshow_with_media(slideshow_id, session)
    if not slideshow:
        return json_response(success=False, message=SLIDESHOW_NOT_FOUND, status_code=404)

    for media in slideshow.media_files:
        if not media.filepath.startswith("/"):
            media.filepath = f"/{settings.UPLOAD_DIR}/{media.filepath}"

    return await render_admin_template(
        request,
        "admin/slideshow_view.html",
        {
            "slideshow": slideshow,
            "max_upload_size_mb": settings.MAX_UPLOAD_SIZE_MB,
            "allowed_media_types": settings.ALLOWED_MEDIA_TYPES,
        },
        user=user
    )


async def set_cover_media(slideshow_id: int, media_id: int, session: AsyncSession, user):
    """Define uma mídia como capa de uma pasta (slideshow)."""
    has_permission = await check_permission(user, "can_set_cover")
    if not has_permission:
        return json_response(success=False, message=NO_PERMISSION_MSG, status_code=403)

    slideshow = await get_slideshow_by_id(slideshow_id, session)
    if not slideshow:
        return json_response(success=False, message=SLIDESHOW_NOT_FOUND, status_code=404)

    slideshow.cover_media_id = media_id
    await session.commit()

    return json_response(success=True, message=SUCCESS_OPERATION)


async def reorder_media(slideshow_id: int, new_order: list[int], session: AsyncSession, user):
    """Atualiza a ordem de exibição das mídias dentro de uma pasta."""

    has_permission = await check_permission(user, "can_reorder_media")
    if not has_permission:
        return json_response(success=False, message=NO_PERMISSION_MSG, status_code=403)

    try:
        valid_ids = await get_media_ids_by_slideshow(slideshow_id, session)

        if not set(new_order).issubset(valid_ids):
            raise HTTPException(status_code=400, detail="Invalid media IDs for this slideshow.")

        for index, media_id in enumerate(new_order):
            await update_media_order(media_id, index + 1, session)

        await session.commit()
        return json_response(success=True, message=SUCCESS_OPERATION)

    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Error updating media order.")


async def update_slideshow_info(slideshow_id: int, data: SlideshowUpdateSchema, session: AsyncSession, user):
    """Atualiza título e descrição de uma pasta existente."""

    has_permission = await check_permission(user, "can_edit_slideshow")
    if not has_permission:
        return json_response(success=False, message=NO_PERMISSION_MSG, status_code=403)

    
    try:
        slideshow = await get_slideshow_by_id(slideshow_id, session)

        if not slideshow:
            return json_response(success=False, message=SLIDESHOW_NOT_FOUND, status_code=404)

        slideshow.title = data.title.strip()
        slideshow.description = (data.description or "").strip()
        await session.commit()

        return json_response(success=True, message=SUCCESS_OPERATION)

    except Exception as e:
        await session.rollback()
        logger.error(f"Erro ao atualizar slideshow: {e}")
        return json_response(success=False, message=SLIDESHOW_CREATION_FAILED, status_code=500)


async def delete_slideshow(slideshow_id: int, session: AsyncSession, user):
    """Remove uma pasta e todos os seus registros relacionados."""
    
    has_permission = await check_permission(user, "can_edit_slideshow")
    if not has_permission:
        return json_response(success=False, message=NO_PERMISSION_MSG, status_code=403)

    
    slideshow = await get_slideshow_by_id(slideshow_id, session)
    if not slideshow:
        return json_response(success=False, message=SLIDESHOW_NOT_FOUND, status_code=404)

    medias = await get_medias_by_slideshow_id(slideshow_id, session)
    all_medias = await get_all_medias(session)

    for media in medias:
        same_file_count = sum(1 for m in all_medias if m.filepath == media.filepath)
        if same_file_count == 1:
            await delete_file(media.filepath)

    await delete_slideshow_and_related(slideshow_id, session)
    return json_response(success=True, message=SUCCESS_OPERATION)
