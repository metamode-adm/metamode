from __future__ import annotations

from datetime import datetime, timezone
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.backend.models.base import Base
from src.backend.core.timezone import convert_to_local_timezone

if TYPE_CHECKING:
    from src.backend.models.role_model import Role
    from src.backend.models.user_slideshow_access_model import UserSlideshowAccess


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(1024), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped["Role"] = relationship(
        back_populates="users"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: convert_to_local_timezone(datetime.now(timezone.utc))
    )

    # Access to specific slideshows
    slideshows_access: Mapped[List[UserSlideshowAccess]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

