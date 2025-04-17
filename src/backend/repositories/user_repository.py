import uuid
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.backend.models.user_model import User
from src.backend.models.role_model import Role


async def get_all_users_db(session: AsyncSession) -> list[User]:
    """Retorna todos os usuários do banco com suas roles."""
    result = await session.execute(
        select(User).options(selectinload(User.role))
    )
    return result.scalars().all()


async def get_user_by_id(session: AsyncSession, user_id: str) -> Optional[User]:
    """Busca um usuário pelo ID com role associada."""
    result = await session.execute(
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.role))
    )
    return result.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: str, exclude_user_id: str = None) -> Optional[User]:
    """Busca um usuário pelo e-mail. Pode excluir um ID da comparação (útil para updates)."""
    stmt = select(User).where(User.email == email).options(selectinload(User.role))
    if exclude_user_id:
        stmt = stmt.where(User.id != exclude_user_id)

    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
    """Busca um usuário pelo nome de usuário com role associada."""
    result = await session.execute(
        select(User)
        .where(User.username == username)
        .options(selectinload(User.role))
    )
    return result.scalar_one_or_none()


async def get_role_by_name(session: AsyncSession, role_name: str) -> Optional[Role]:
    """Busca uma role pelo nome."""
    result = await session.execute(select(Role).where(Role.name == role_name))
    return result.scalar_one_or_none()


async def create_user_db(
    session: AsyncSession,
    username: str,
    email: str,
    hashed_password: str,
    is_active: bool,
    role_name: str,
) -> User:
    """Cria e persiste um novo usuário no banco com a role associada."""
    role = await get_role_by_name(session, role_name)
    if not role:
        raise ValueError(f"Role '{role_name}' não encontrada.")

    new_user = User(
        id=str(uuid.uuid4()),
        username=username,
        email=email,
        hashed_password=hashed_password,
        is_active=is_active,
        role=role,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def delete_user_db(session: AsyncSession, user: User) -> None:
    """Deleta um usuário do banco."""
    await session.delete(user)
    await session.commit()


async def update_user_db(session: AsyncSession, user: User) -> None:
    """Atualiza os dados de um usuário existente."""
    session.add(user)
    await session.commit()
    await session.refresh(user)
