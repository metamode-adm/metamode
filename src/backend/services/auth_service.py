import time
import re
import logging
from fastapi import HTTPException, status, Request, Depends
from src.backend.models.role_model import Role  
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.backend.models.user_model import User
from src.backend.core.responses import set_flash_message
from src.backend.core.messages import (
    LOGIN_REQUIRED,
    LOGIN_ERROR_INVALID_CREDENTIALS,
    NO_ADMIN_PERMISSION,
)
from src.backend.core.database import get_db
from sqlalchemy.exc import SQLAlchemyError


logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """Gera um hash seguro para a senha usando Argon2."""
    return pwd_context.hash(password)


def is_password_strong(password: str) -> bool:
    """Verifica se a senha atende aos critérios de segurança."""
    return (
        len(password) >= 8
        and re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"\d", password)
        and re.search(r"[!@#$%^&*]", password)
    )


async def get_user_by_username(username: str, session: AsyncSession) -> User | None:
    """Busca um usuário pelo username no banco de dados."""
    result = await session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def authenticate_user(username: str, password: str, session: AsyncSession) -> tuple[User | None, bool]:
    """
    Autentica o usuário verificando nome e senha.
    Retorna uma tupla: (usuário ou None, erro interno ou não).
    """
    try:
        user = await get_user_by_username(username, session)

        if not user:
            logger.warning(f"Falha de autenticação: usuário '{username}' não encontrado.")
            return None, False

        if not user.is_active:
            logger.warning(f"Usuário '{username}' está inativo.")
            return None, False

        if not pwd_context.verify(password, user.hashed_password):
            logger.warning(f"Senha incorreta para o usuário '{username}'.")
            return None, False

        logger.info(f"Usuário '{username}' autenticado com sucesso.")
        return user, False

    except Exception as e:
        logger.error(f"Erro interno ao autenticar o usuário '{username}': {e}")
        return None, True


def is_ajax(request: Request) -> bool:
    """Verifica se a requisição é assíncrona (AJAX)."""
    return request.headers.get("accept") == "application/json"


async def load_logged_in_user_with_permissions(request: Request, session: AsyncSession) -> User:
    """
    Carrega o usuário autenticado da sessão como modelo SQLAlchemy com role e permissions.
    Reforçado contra erro de conexão e sessão corrompida.
    """
    try:
        user_id = request.session.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail=LOGIN_REQUIRED)

        result = await session.execute(
            select(User)
            .options(joinedload(User.role).joinedload(Role.permissions))
            .where(User.id == user_id)
        )

        user = result.scalar_one_or_none()

        if not user or not user.role or not user.role.permissions:
            raise HTTPException(status_code=403, detail=NO_ADMIN_PERMISSION)

        return user

    except HTTPException as http_exc:
        # Repassa a exceção para ser tratada no handler correto
        raise http_exc

    except SQLAlchemyError as db_exc:
        logger.error(f"Erro de banco ao carregar usuário autenticado: {db_exc}")
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco de dados.")

    except Exception as e:
        logger.error(f"Erro inesperado ao carregar usuário autenticado: {e}")
        raise HTTPException(status_code=500, detail="Erro interno inesperado.")


async def get_current_user_with_permissions(
    request: Request,
    session: AsyncSession = Depends(get_db)
) -> User:
    """Dependency para obter o usuário autenticado com role e permissions carregados."""
    return await load_logged_in_user_with_permissions(request, session)