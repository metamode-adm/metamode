import asyncio
import logging
import sys
import os

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.backend.models.role_model import Role
from src.backend.models.permission_model import Permission
from src.backend.core.database import async_session_maker

# Configuração do logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # Define o nível de log para INFO

# Função que cria as roles padrão no banco
async def create_roles(session: AsyncSession):
    logger.info("Criando roles padrão...")

    # Verifica se as roles já existem
    existing_roles = await session.execute(select(Role.name))
    existing_roles_names = {role[0] for role in existing_roles.fetchall()}

    roles = ['comum', 'admin', 'superadmin']
    
    for role_name in roles:
        if role_name not in existing_roles_names:
            role = Role(name=role_name)
            session.add(role)
            logger.info(f"Role '{role_name}' criada.")
    
    await session.commit()

# Função que cria as permissões associadas a cada role
async def create_permissions(session: AsyncSession):
    logger.info("Criando permissões padrão...")

    # Recupera todas as roles
    roles = await session.execute(select(Role.id, Role.name))
    roles = roles.fetchall()

    for role_id, role_name in roles:
        logger.info(f"Criando permissões para o papel: {role_name}")

        if role_name == 'comum':
            permissions = {
                'can_view_slideshow': False,
                'can_create_slideshow': False,
                'can_edit_slideshow': False,
                'can_view_sharing': False,
                'can_add_users_to_slideshow': False,
                'can_view_media': True,
                'can_upload_media': False,
                'can_delete_media': False,
                'can_reorder_media': False,
                'can_set_cover': False,
                'can_create_user': False,
                'can_create_superadmin': False,
                'can_remove_user': False,
                'can_remove_admins': False,
                'can_edit_roles': False,
                'can_view_user_slideshows': False,
                'can_remove_user_from_slideshow': False,
                'can_edit_own_profile': True,
                'can_view_carousel': True,
                'can_share_slideshow': False,
                'can_search_users': False,
            }

        elif role_name == 'admin':
            permissions = {
                'can_view_slideshow': True,
                'can_create_slideshow': True,
                'can_edit_slideshow': True,
                'can_view_sharing': True,
                'can_add_users_to_slideshow': True,
                'can_view_media': True,
                'can_upload_media': True,
                'can_delete_media': True,
                'can_reorder_media': True,
                'can_set_cover': True,
                'can_create_user': True,
                'can_create_superadmin': False,
                'can_remove_user': True,
                'can_remove_admins': True,
                'can_edit_roles': True,
                'can_view_user_slideshows': True,
                'can_remove_user_from_slideshow': True,
                'can_edit_own_profile': True,
                'can_view_carousel': True,
                'can_share_slideshow': True,
                'can_search_users': True,
            }

        elif role_name == 'superadmin':
            permissions = {
                'can_view_slideshow': True,
                'can_create_slideshow': True,
                'can_edit_slideshow': True,
                'can_view_sharing': True,
                'can_add_users_to_slideshow': True,
                'can_view_media': True,
                'can_upload_media': True,
                'can_delete_media': True,
                'can_reorder_media': True,
                'can_set_cover': True,
                'can_create_user': True,
                'can_create_superadmin': True,
                'can_remove_user': True,
                'can_remove_admins': True,
                'can_edit_roles': True,
                'can_view_user_slideshows': True,
                'can_remove_user_from_slideshow': True,
                'can_edit_own_profile': True,
                'can_view_carousel': True,
                'can_share_slideshow': True,
                'can_search_users': True,
            }

        permission = Permission(role_id=role_id, **permissions)
        session.add(permission)
        logger.info(f"Permissões para role '{role_name}' criadas.")

    await session.commit()

# Função principal para rodar o processo de seed
async def seed_data():
    async with async_session_maker() as session:
        await create_roles(session)
        await create_permissions(session)

if __name__ == "__main__":
    logger.info("Iniciando o script de seed de roles e permissões...")
    asyncio.run(seed_data())
    logger.info("Seed de roles e permissões concluído!")
