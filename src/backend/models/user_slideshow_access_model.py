from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.backend.models.base import Base

if TYPE_CHECKING:
    from src.backend.models.user_model import User
    from src.backend.models.role_model import Role
    from src.backend.models.slideshow_model import Slideshow


class UserSlideshowAccess(Base):
    __tablename__ = "user_slideshow_access"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    slideshow_id: Mapped[int] = mapped_column(
        ForeignKey("slideshows.id", ondelete="CASCADE"), nullable=False
    )

    can_edit: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    user: Mapped[User] = relationship(back_populates="slideshows_access")
    slideshow: Mapped[Slideshow] = relationship(back_populates="access_list")
