from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.core.database import get_db
from src.backend.models.user_model import User
from src.backend.services.auth_service import get_current_user_with_permissions
from src.backend.schemas.user_schema import UserUpdateProfileSchema, UserUpdatePasswordSchema
from src.backend.services.user_profile_service import (
    render_profile_page,
    update_profile_data,
    update_profile_password,
)

router = APIRouter()


@router.get("/profile")
async def profile_page(
    request: Request,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions),
):
    """Renderiza a tela de perfil do usuário logado."""
    return await render_profile_page(request, session, user)


@router.put("/profile/update")
async def update_profile(
    data: UserUpdateProfileSchema,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions),
):
    """Atualiza o nome de usuário ou e-mail do próprio usuário."""
    return await update_profile_data(data, session, user)


@router.put("/profile/password")
async def change_password(
    data: UserUpdatePasswordSchema,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions),
):
    """Atualiza a senha do próprio usuário."""
    return await update_profile_password(data, session, user)
