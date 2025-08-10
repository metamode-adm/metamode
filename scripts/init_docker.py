#!/usr/bin/env python3
"""
Script de inicialização para Docker do Metamode
Executa migrações e seeds automaticamente se AUTO_INIT_DB=true
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_command(command, description):
    """Executa um comando e retorna True se bem-sucedido"""
    try:
        logger.info(f"🚀 {description}...")
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        logger.info(f"✅ {description} concluído com sucesso")
        if result.stdout:
            logger.info(f"Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Erro em {description}: {e}")
        if e.stdout:
            logger.error(f"Stdout: {e.stdout}")
        if e.stderr:
            logger.error(f"Stderr: {e.stderr}")
        return False

def check_database_connection():
    """Verifica se é possível conectar ao banco de dados"""
    try:
        # Importa e testa a conexão com o banco
        sys.path.append('/app')
        from src.backend.core.database import async_session_maker
        import asyncio
        
        async def test_connection():
            from sqlalchemy import text
            async with async_session_maker() as session:
                await session.execute(text('SELECT 1'))
                return True
        
        result = asyncio.run(test_connection())
        logger.info("✅ Conexão com banco de dados verificada")
        return result
    except Exception as e:
        logger.error(f"❌ Erro ao conectar com banco de dados: {e}")
        return False

def main():
    """Função principal de inicialização"""
    logger.info("🔧 Iniciando script de inicialização do Docker")
    
    # Verifica a variável AUTO_INIT_DB
    auto_init = os.getenv('AUTO_INIT_DB', 'false').lower() == 'true'
    
    if not auto_init:
        logger.info("⏭️ AUTO_INIT_DB=false - Pulando inicialização automática")
        logger.info("📋 Execute manualmente:")
        logger.info("   1. alembic upgrade head")
        logger.info("   2. PYTHONPATH=. python scripts/seed_roles_and_permissions.py")
        logger.info("   3. PYTHONPATH=. python scripts/seed_default_users.py")
        return True
    
    logger.info("🚀 AUTO_INIT_DB=true - Executando inicialização automática")
    
    # Aguarda um pouco para o banco estar pronto
    import time
    logger.info("⏳ Aguardando banco de dados estar pronto...")
    time.sleep(5)
    
    # Verifica conexão com banco
    if not check_database_connection():
        logger.error("❌ Não foi possível conectar ao banco de dados")
        return False
    
    # Executa migrações
    if not run_command("alembic upgrade head", "Aplicando migrações do banco"):
        return False
    
    # Executa seed de roles e permissões
    if not run_command(
        "PYTHONPATH=. python scripts/seed_roles_and_permissions.py",
        "Criando roles e permissões padrão"
    ):
        return False
    
    # Executa seed de usuários padrão
    if not run_command(
        "PYTHONPATH=. python scripts/seed_default_users.py",
        "Criando usuários padrão"
    ):
        return False
    
    logger.info("🎉 Inicialização automática concluída com sucesso!")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        logger.error("💥 Falha na inicialização - verifique os logs acima")
        sys.exit(1)
    
    logger.info("✅ Script de inicialização finalizado")