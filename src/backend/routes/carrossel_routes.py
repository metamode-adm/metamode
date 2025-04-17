from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.core.database import get_db
from src.backend.core.templates import templates
from src.backend.services.auth_service import get_current_user_with_permissions
from src.backend.services.carousel_service import get_carousel_context
from src.backend.core.messages import LOGIN_REQUIRED
from src.backend.models.user_model import User
from src.backend.core.responses import set_flash_message

import logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/carousel")
async def carousel_page(
    request: Request,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions)
):
    """Renderiza o carrossel com as mídias do usuário logado."""
    context, error_code = await get_carousel_context(request, session, user)

    if error_code == "NO_PERMISSION":
        set_flash_message(request, "Você não tem permissão para visualizar o carrossel.")
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse("carousel.html", context)
