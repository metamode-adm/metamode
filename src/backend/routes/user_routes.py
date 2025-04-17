from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.core.database import get_db
from src.backend.services.auth_service import get_current_user_with_permissions
from src.backend.services.user_service import (
    list_all_users,
    create_new_user,
    delete_user,
    update_user_data,
)
from src.backend.schemas.user_schema import UserCreateSchema, UserUpdateSchema
from src.backend.models.user_model import User

router = APIRouter()


@router.get("/admin/usuarios")
async def user_management(
    request: Request,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions),
):
    """Renderiza a tela de gerenciamento de usuários com dados."""
    return await list_all_users(request, session, user)

@router.post("/admin/usuarios")
async def create_user(
    user_data: UserCreateSchema,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions),
):
    """Cria um novo usuário."""
    return await create_new_user(user_data, session, user)


@router.delete("/admin/usuarios/{user_id}")
async def remove_user(
    user_id: str,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions),
):
    """Remove um usuário existente."""
    return await delete_user(user_id, session, user)


@router.put("/admin/usuarios/{user_id}")
async def update_user(
    user_id: str,
    user_data: UserUpdateSchema,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_with_permissions),
):
    """Atualiza os dados de um usuário existente."""
    return await update_user_data(user_id, user_data, session, user)
