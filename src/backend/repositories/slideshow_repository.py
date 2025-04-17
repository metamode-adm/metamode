import logging
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from src.backend.models.slideshow_model import Slideshow
from src.backend.models.media_model import Media
from src.backend.models.user_slideshow_access_model import UserSlideshowAccess
from src.backend.core.timezone import convert_to_local_timezone
logger = logging.getLogger(__name__)


async def get_all_slideshows_with_cover(session: AsyncSession):
    """Retorna todos os slideshows com capa, mídias e acessos."""
    try:
        result = await session.execute(
            select(Slideshow)
            .options(
                selectinload(Slideshow.cover),
                selectinload(Slideshow.media_files),
                selectinload(Slideshow.access_list)
            )
            .order_by(Slideshow.created_at.desc())
        )
        return result.scalars().all()
    except Exception as e:
        logger.error(f"Erro ao buscar slideshows: {e}")
        return []


async def get_slideshow_with_media(slideshow_id: int, session: AsyncSession):
    """Retorna um slideshow com mídias ordenadas."""
    try:
        result = await session.execute(
            select(Slideshow)
            .options(selectinload(Slideshow.media_files))
            .where(Slideshow.id == slideshow_id)
        )
        slideshow = result.scalars().first()

        if slideshow and slideshow.media_files:
            slideshow.media_files.sort(key=lambda m: m.order or 0)

        return slideshow
    except Exception as e:
        logger.error(f"Erro ao buscar slideshow {slideshow_id}: {e}")
        return None


async def get_slideshow_by_id(slideshow_id: int, session: AsyncSession) -> Slideshow | None:
    """Retorna slideshow simples por ID."""
    result = await session.execute(
        select(Slideshow).where(Slideshow.id == slideshow_id)
    )
    return result.scalar_one_or_none()


async def get_slideshows_shared_with_user(session: AsyncSession, user_id: str) -> list[Slideshow]:
    """
    Retorna os slideshows que estão compartilhados com o usuário informado.
    """
    try:
        result = await session.execute(
            select(Slideshow)
            .join(UserSlideshowAccess)
            .options(
                selectinload(Slideshow.cover),
                selectinload(Slideshow.media_files),
                selectinload(Slideshow.access_list),
            )
            .where(UserSlideshowAccess.user_id == user_id)
        )
        return result.scalars().all()
    except Exception as e:
        logger.error(f"Erro ao buscar slideshows compartilhados com usuário {user_id}: {e}")
        return []


async def create_slideshow_db(data, session: AsyncSession) -> Slideshow:
    """Cria novo slideshow com data convertida."""
    novo = Slideshow(
        name=data.name,
        title=data.title,
        description=data.description,
        created_at=convert_to_local_timezone(datetime.now(timezone.utc))
    )
    session.add(novo)
    await session.commit()
    await session.refresh(novo)
    return novo


async def get_media_ids_by_slideshow(slideshow_id: int, session: AsyncSession) -> set[int]:
    """Busca os IDs das mídias associadas a um slideshow."""
    result = await session.execute(
        select(Media.id).where(Media.slideshow_id == slideshow_id)
    )
    return {row[0] for row in result.fetchall()}


async def update_media_order(media_id: int, order: int, session: AsyncSession):
    """Atualiza o campo de ordenação da mídia."""
    await session.execute(
        update(Media)
        .where(Media.id == media_id)
        .values(order=order)
    )


async def get_medias_by_slideshow_id(slideshow_id: int, session: AsyncSession):
    """Retorna todas as mídias de um slideshow específico."""
    result = await session.execute(
        select(Media).where(Media.slideshow_id == slideshow_id)
    )
    return result.scalars().all()


async def get_all_medias(session: AsyncSession):
    """Retorna todas as mídias do sistema."""
    result = await session.execute(select(Media))
    return result.scalars().all()


async def delete_slideshow_and_related(slideshow_id: int, session: AsyncSession):
    """Remove mídias, permissões e o slideshow em si."""

    # Desvincula a capa para evitar erro de foreign key
    await session.execute(
        update(Slideshow)
        .where(Slideshow.id == slideshow_id)
        .values(cover_media_id=None)
    )

    # Remove mídias associadas à pasta
    await session.execute(delete(Media).where(Media.slideshow_id == slideshow_id))

    # Remove permissões de acesso
    await session.execute(delete(UserSlideshowAccess).where(UserSlideshowAccess.slideshow_id == slideshow_id))

    # Remove o próprio slideshow
    result = await session.execute(select(Slideshow).where(Slideshow.id == slideshow_id))
    slideshow = result.scalar_one_or_none()
    if slideshow:
        await session.delete(slideshow)

    await session.commit()