from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.backend.models.media_model import Media
import logging
from sqlalchemy.orm import joinedload
from src.backend.models.media_model import Media
from src.backend.models.slideshow_model import Slideshow
from src.backend.models.user_slideshow_access_model import UserSlideshowAccess
logger = logging.getLogger(__name__)


async def save_media_db(media: Media, session: AsyncSession):
    """Salva a mídia no banco de dados."""
    session.add(media)
    await session.commit()
    return media


async def get_all_media(session: AsyncSession):
    """Retorna todas as mídias cadastradas no banco."""
    async with session.begin():
        result = await session.execute(select(Media))
        return result.scalars().all()  


async def get_media_by_user_access(user_id: str, session: AsyncSession):
    """Busca mídias de slideshows associados ao usuário, ordenadas por ordem definida."""
    result = await session.execute(
        select(Media)
        .join(Slideshow, Media.slideshow_id == Slideshow.id)
        .join(UserSlideshowAccess, UserSlideshowAccess.slideshow_id == Slideshow.id)
        .where(UserSlideshowAccess.user_id == user_id)
        .order_by(Slideshow.id, Media.order.asc())
        .options(joinedload(Media.slideshow)) 
    )
    return result.scalars().all()


async def get_media_by_id(media_id: int, session: AsyncSession):
    """Busca uma mídia pelo ID."""
    query = select(Media).where(Media.id == media_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def delete_media_by_id(media_id: int, session: AsyncSession) -> bool:
    """Remove uma mídia do banco de dados."""
    result = await session.execute(select(Media).filter(Media.id == media_id))
    media = result.scalars().first()

    if not media:
        logger.error(f"🗑️ Não foi possível excluir a mídia do banco de dados: {media_id}")
        return False

    try:
        await session.delete(media)
        await session.commit()
        logger.info(f"🗑️ Mídia excluída do banco de dados: {media_id}")
        return True

    except Exception as e:
        await session.rollback()
        logger.error(f"Erro ao excluir mídia ID {media_id}: {e}")
        return False
    

async def is_media_shared(media_id: int, session: AsyncSession) -> tuple[Media | None, bool]:
    """
    Retorna a mídia pelo ID e informa se o arquivo (filepath) dela é compartilhado por outras mídias.
    """
    result = await session.execute(select(Media))
    all_medias = result.scalars().all()

    media = next((m for m in all_medias if m.id == media_id), None)
    if not media:
        return None, False

    shared_count = sum(1 for m in all_medias if m.filepath == media.filepath)
    return media, shared_count > 1
