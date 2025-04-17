from src.backend.models.user_model import User
from src.backend.core import messages
import logging

logger = logging.getLogger(__name__)


async def check_permission(user: User, permission_name: str) -> bool:
    """Verifica se o usuário possui determinada permissão ligada ao seu papel."""
    logger.debug(f"Verificando permissão '{permission_name}' para o usuário '{user.username}'")

    if not user.role or not user.role.permissions:
        logger.warning(f"Usuário '{user.username}' não possui permissão para '{permission_name}'.")
        return False  # Retorna False para indicar falta de permissão

    permission = getattr(user.role.permissions, permission_name, None)

    if permission is None or not permission:
        logger.warning(f"Permissão '{permission_name}' negada ou nao encontrada para o usuário '{user.username} - result: {permission}'.")
        return False  # Retorna False para indicar falta de permissão

    return True  # Se a permissão for encontrada e for True

