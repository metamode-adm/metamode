from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.backend.core.config import settings

# Criando o motor de conexão assíncrona com MySQL
engine = create_async_engine(
    settings.DATABASE_URL, # URL do banco de dados obtida das configurações
    echo=False,  # Ativa o log de todas as operações SQL 
    pool_pre_ping=True,     # Ativa o envio de pings para verificar se as conexões no pool ainda estão ativas
    pool_recycle=28000,     # Tempo em segundos para reciclar conexões inativas no pool (evita desconexões)
    pool_size=20,           # Número máximo de conexões persistentes no pool
    max_overflow=10,        # Número máximo de conexões extras além do pool_size permitido
)

# Criando o gerenciador de sessões assíncronas
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependência para FastAPI: gera uma nova sessão do banco de dados a cada requisição
async def get_db():
    async with async_session_maker() as session:
        yield session
