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


async def authenticate_user(username: str, password: str, session: AsyncSession) -> User | None:
    """Autentica o usuário verificando nome e senha."""
    user = await get_user_by_username(username, session)

    if not user:
        logger.warning(f"Falha de autenticação: usuário '{username}' não encontrado.")
        return None

    if not user.is_active:
        logger.warning(f"Usuário '{username}' está inativo.")
        return None

    if not pwd_context.verify(password, user.hashed_password):
        logger.warning(f"Senha incorreta para o usuário '{username}'.")
        return None

    logger.info(f"Usuário '{username}' autenticado com sucesso.")
    return user


def is_ajax(request: Request) -> bool:
    """Verifica se a requisição é assíncrona (AJAX)."""
    return request.headers.get("accept") == "application/json"


async def verificar_login(request: Request) -> dict:
    """Verifica se o usuário está logado e se a sessão é válida."""
    user = request.session.get("user")

    if not user or not isinstance(user, dict):
        logger.info("Sessão ausente ou inválida. Redirecionando para login.")
        request.session.clear()
        if is_ajax(request):
            return JSONResponse(status_code=401, content={"success": False, "message": LOGIN_REQUIRED})
        set_flash_message(request, LOGIN_REQUIRED)
        raise HTTPException(status_code=303, headers={"Location": "/login"})

    if "username" not in user or "is_admin" not in user or "is_super_admin" not in user:
        logger.warning("Sessão corrompida ou incompleta. Redirecionando para login.")
        request.session.clear()
        if is_ajax(request):
            return JSONResponse(status_code=401, content={"success": False, "message": LOGIN_REQUIRED})
        set_flash_message(request, LOGIN_REQUIRED)
        raise HTTPException(status_code=303, headers={"Location": "/login"})

    if user.get("expires") and time.time() > user["expires"]:
        logger.info(f"Sessão expirada para o usuário '{user.get('username')}'.")
        request.session.clear()
        if is_ajax(request):
            return JSONResponse(status_code=401, content={"success": False, "message": LOGIN_REQUIRED})
        set_flash_message(request, LOGIN_REQUIRED)
        raise HTTPException(status_code=303, headers={"Location": "/login"})

    logger.debug(f"Usuário '{user.get('username')}' com sessão válida.")
    return user


async def verificar_super_admin(request: Request) -> dict:
    """Verifica se o usuário é um Super Admin."""
    user = await verificar_login(request)

    if not user.get("is_super_admin"):
        logger.warning(f"Usuário '{user.get('username')}' tentou acessar rota de Super Admin sem permissão.")
        set_flash_message(request, NO_ADMIN_PERMISSION)
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/login"})

    logger.info(f"Usuário '{user.get('username')}' é Super Admin.")
    return user


async def load_logged_in_user_with_permissions(request: Request, session: AsyncSession) -> User:
    """
    Carrega o usuário autenticado da sessão como modelo SQLAlchemy com role e permissions.
    """
    user_id = request.session.get("user_id")

    if not user_id:
        raise HTTPException(status_code=401, detail=LOGIN_REQUIRED)

    result = await session.execute(
        select(User)
        .options(
            joinedload(User.role).joinedload(Role.permissions) 
            
        )
        .where(User.id == user_id)
    )
    
    
    user = result.scalar_one_or_none()

    if not user or not user.role or not user.role.permissions:
        raise HTTPException(status_code=403, detail=NO_ADMIN_PERMISSION)

    return user


async def get_current_user_with_permissions(
    request: Request,
    session: AsyncSession = Depends(get_db)
) -> User:
    """Dependency para obter o usuário autenticado com role e permissions carregados."""
    return await load_logged_in_user_with_permissions(request, session)