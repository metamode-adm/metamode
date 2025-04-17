from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.backend.models.base import Base
from src.backend.core.timezone import convert_to_local_timezone

if TYPE_CHECKING:
    from src.backend.models.slideshow_model import Slideshow


class Media(Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    filepath: Mapped[str] = mapped_column(String(500), nullable=False)
    file_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    size_mb: Mapped[float] = mapped_column(nullable=False)
    duration: Mapped[Optional[int]] = mapped_column(nullable=True)

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: convert_to_local_timezone(datetime.now(timezone.utc))
    )

    slideshow_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("slideshows.id", ondelete="SET NULL"),
        nullable=True
    )

    order: Mapped[Optional[int]] = mapped_column(nullable=True)

    # Relationships
    slideshow: Mapped[Optional[Slideshow]] = relationship(
        back_populates="media_files",
        foreign_keys=[slideshow_id]
    )

    as_cover_for: Mapped[Optional[Slideshow]] = relationship(
        back_populates="cover",
        uselist=False,
        foreign_keys="Slideshow.cover_media_id"
    )
