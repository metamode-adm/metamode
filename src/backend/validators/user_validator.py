from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.backend.models.user_model import User


async def is_email_already_used(session: AsyncSession, email: str, exclude_user_id: str = None) -> bool:
    """
    Verifica se o e-mail já está em uso, opcionalmente ignorando um user_id (em casos de update).
    """
    query = select(User).where(User.email == email)
    if exclude_user_id:
        query = query.where(User.id != exclude_user_id)

    result = await session.execute(query)
    return result.scalars().first() is not None

