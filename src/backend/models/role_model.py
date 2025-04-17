from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.backend.models.base import Base

if TYPE_CHECKING:
    from src.backend.models.permission_model import Permission
    from src.backend.models.user_model import User


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    permissions: Mapped[Permission] = relationship(
        back_populates="role",
        uselist=False,
        cascade="all, delete-orphan"
    )

    users: Mapped[list[User]] = relationship(
        back_populates="role"
    )
