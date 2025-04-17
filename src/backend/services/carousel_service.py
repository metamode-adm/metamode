import logging
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.core.config import settings
from src.backend.repositories.media_repository import get_media_by_user_access
from src.backend.core.responses import get_flash_message
from src.backend.services.permission_service import check_permission
from src.backend.models.user_model import User  # ✅ agora tipamos como modelo
from src.backend.core.responses import json_response
from src.backend.core.messages import NO_PERMISSION_MSG
from fastapi.responses import RedirectResponse
from fastapi import HTTPException, status
logger = logging.getLogger(__name__)

async def get_carousel_context(request: Request, session: AsyncSession, user: User):
    """Retorna o contexto necessário para exibir o carrossel de mídias do usuário logado."""
    
    has_permission = await check_permission(user, "can_view_carousel")
    if not has_permission:
        return RedirectResponse(url="/no-permission", status_code=status.HTTP_303_SEE_OTHER)

    media_list = await get_media_by_user_access(user.id, session)

    for media in media_list:
        if not media.filepath.startswith("/"):
            media.filepath = f"/{settings.UPLOAD_DIR}/{media.filepath}"

    error = get_flash_message(request)

    return {
        "request": request,
        "user": user,
        "midias": media_list,
        "error": error
    }, None
