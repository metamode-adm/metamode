from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.backend.models.base import Base
from src.backend.core.timezone import convert_to_local_timezone

if TYPE_CHECKING:
    from src.backend.models.media_model import Media
    from src.backend.models.user_slideshow_access_model import UserSlideshowAccess


class Slideshow(Base):
    __tablename__ = "slideshows"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    cover_media_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("media.id"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: convert_to_local_timezone(datetime.now(timezone.utc))
    )

    # Relationships
    media_files: Mapped[List[Media]] = relationship(
        back_populates="slideshow",
        cascade="all, delete-orphan",
        foreign_keys="Media.slideshow_id"  
    )

    cover: Mapped[Optional[Media]] = relationship(
        back_populates="as_cover_for",
        foreign_keys=[cover_media_id],
        uselist=False
    )

    access_list: Mapped[List[UserSlideshowAccess]] = relationship(
        back_populates="slideshow",
        cascade="all, delete-orphan"
    )


