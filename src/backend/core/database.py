from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.backend.core.config import settings

# Criando o motor de conexão assíncrona com MySQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
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
