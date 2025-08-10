import asyncio
import uuid
import logging
import sys
import os

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from src.backend.core.database import async_session_maker
from src.backend.models.user_model import User
from src.backend.models.role_model import Role
from src.backend.services.user_service import hash_password

# Configuração do logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # Define o nível de log para INFO

async def seed_default_users(session):
    """
    Cria os usuários padrões (superadmin, admin, comum) com base nas roles criadas.
    """
    logger.info("Iniciando a criação de usuários padrões.")

    # Carregar as roles já existentes
    roles_map = {}
    result = await session.execute(select(Role).where(Role.name.in_(['superadmin', 'admin', 'comum'])))
    roles = result.scalars().all()

    for role in roles:
        roles_map[role.name] = role

    # Criar os usuários com as roles correspondentes
    users = [
        {
            "username": "admin",
            "password": "admin123",
            "role": roles_map.get("superadmin")
        },

    ]

    for user_data in users:
        result = await session.execute(select(User).where(User.username == user_data["username"]))
        if result.scalar_one_or_none():
            logger.info(f"🔁 Usuário '{user_data['username']}' já existe. Pulando...")
            continue

        user = User(
            id=str(uuid.uuid4()),
            username=user_data["username"],
            email=f"{user_data['username']}@example.com",
            hashed_password=hash_password(user_data["password"]),
            is_active=True,
            role_id=user_data["role"].id
        )
        session.add(user)
        logger.info(f"Usuário '{user_data['username']}' criado com sucesso.")

    await session.commit()
    logger.info("✅ Usuários padrão criados com sucesso!")

# Função principal para rodar o processo de seed
async def main():
    async with async_session_maker() as session:
        await seed_default_users(session)

if __name__ == "__main__":
    logger.info("🚀 Iniciando o script para seed dos usuários padrão...")
    asyncio.run(main())
    logger.info("🔒 Por segurança, remova este script após o uso!")
