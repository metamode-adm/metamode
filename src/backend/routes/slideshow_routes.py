from fastapi import APIRouter, Request, Depends, Body, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.backend.core.database import get_db
from src.backend.models.user_model import User
from src.backend.services.auth_service import get_current_user_with_permissions
from src.backend.services import (
    slideshow_service,
    access_service,
    media_service
)
from src.backend.schemas.slideshow_schema import SlideshowCreateSchema, SlideshowUpdateSchema

router = APIRouter()



@router.get("/admin/media")
async def list_slideshows(
    request: Request,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions)
):
    return await slideshow_service.list_slideshows(request, session, user)


@router.post("/admin/media")
async def create_slideshow(
    data: SlideshowCreateSchema,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions)
):
    return await slideshow_service.create_slideshow(data, session, user)


@router.get("/admin/media/{slideshow_id}")
async def view_slideshow(
    slideshow_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions)
):
    return await slideshow_service.view_slideshow(slideshow_id, request, session, user)


@router.put("/admin/media/{slideshow_id}/update")
async def update_slideshow_info(
    slideshow_id: int,
    data: SlideshowUpdateSchema,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions)
):
    return await slideshow_service.update_slideshow_info(slideshow_id, data, session, user)


@router.delete("/admin/slideshow/{slideshow_id}")
async def delete_slideshow(
    slideshow_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions)
):
    return await slideshow_service.delete_slideshow(slideshow_id, session, user)



@router.post("/admin/media/{slideshow_id}/upload")
async def upload_to_slideshow(
    slideshow_id: int,
    request: Request,
    files: List[UploadFile],
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions)
):
    return await media_service.upload_to_slideshow(slideshow_id, request, files, session, user)


@router.post("/admin/media/{slideshow_id}/set-cover/{media_id}")
async def set_cover_media(
    slideshow_id: int,
    media_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions)
):
    return await slideshow_service.set_cover_media(slideshow_id, media_id, session, user)


@router.post("/admin/media/{slideshow_id}/reorder")
async def reorder_media(
    slideshow_id: int,
    new_order: List[int] = Body(...),
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions)
):
    return await slideshow_service.reorder_media(slideshow_id, new_order, session, user)


@router.delete("/admin/media/{media_id}")
async def delete_media(
    media_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions)
):
    return await media_service.delete_media(media_id, session, user)



@router.get("/admin/media/{slideshow_id}/access")
async def get_slideshow_access_info(
    slideshow_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions)
):
    return await access_service.get_slideshow_access_info(slideshow_id, session, user)


@router.post("/admin/media/{slideshow_id}/access/add")
async def add_user_to_slideshow_access(
    slideshow_id: int,
    data: dict = Body(...),
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions)
):
    return await access_service.add_user_to_slideshow_access(slideshow_id, data, session, user)


@router.delete("/admin/media/{slideshow_id}/access/remove/{user_id}")
async def remove_user_from_slideshow_access(
    slideshow_id: int,
    user_id: str,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions)
):
    return await access_service.remove_user_from_slideshow_access(slideshow_id, user_id, session, user)



@router.get("/admin/users/search")
async def search_users_for_slideshow(
    q: str,
    slideshow_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions)
):
    return await access_service.search_users_for_slideshow(q, slideshow_id, session, user)


@router.get("/admin/users/{user_id}/slideshows")
async def get_user_slideshows(
    user_id: str,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions)
):
    return await access_service.get_user_slideshows(user_id, session, user)
