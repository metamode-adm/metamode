import sys
import os
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# Garante que a pasta raiz do projeto esteja no sys.path
sys.path.append(os.path.abspath("."))

# Configuração do Alembic (do alembic.ini)
config = context.config

# Configura logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Importa os metadados
from src.backend.core.config import settings
from src.backend.models.base import Base

target_metadata = Base.metadata

# URL do banco de dados do arquivo de configuração do projeto
DATABASE_URL = settings.DATABASE_URL

def do_run_migrations(connection):
    """Executa as migrações com a conexão ativa."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # Detecta mudanças de tipo nas colunas
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Executa as migrações com engine assíncrona."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = DATABASE_URL

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def run_migrations_offline():
    """Executa as migrações em modo offline."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

# 🚦 Decide se executa online ou offline
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
