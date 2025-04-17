from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.backend.models.base import Base

if TYPE_CHECKING:
    from src.backend.models.role_model import Role


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), unique=True)

    # SlideShow
    can_view_slideshow: Mapped[bool] = mapped_column(Boolean, default=True)   # Permissão para visualizar slideshows
    can_create_slideshow: Mapped[bool] = mapped_column(Boolean, default=False)  # Permissão para criar slideshows
    can_edit_slideshow: Mapped[bool] = mapped_column(Boolean, default=False)    # Permissão para editar slideshows
    can_view_sharing: Mapped[bool] = mapped_column(Boolean, default=False)      # Permissão para visualizar compartilhamentos
    can_add_users_to_slideshow: Mapped[bool] = mapped_column(Boolean, default=False)  # Permissão para adicionar usuários a slideshows
    can_share_slideshow: Mapped[bool] = mapped_column(Boolean, default=False) # Permissão para compartilhar slideshows
    can_search_users: Mapped[bool] = mapped_column(Boolean, default=False)    # Permissão para buscar usuários

    # Gerenciar Mídia
    can_view_media: Mapped[bool] = mapped_column(Boolean, default=True)         # Permissão para visualizar mídias
    can_upload_media: Mapped[bool] = mapped_column(Boolean, default=False)     # Permissão para fazer upload de mídias
    can_delete_media: Mapped[bool] = mapped_column(Boolean, default=False)     # Permissão para deletar mídias
    can_reorder_media: Mapped[bool] = mapped_column(Boolean, default=False)    # Permissão para reordenar mídias
    can_set_cover: Mapped[bool] = mapped_column(Boolean, default=False)        # Permissão para definir a capa de uma mídia

    # Usuários
    can_create_user: Mapped[bool] = mapped_column(Boolean, default=False)      # Permissão para criar novos usuários
    can_create_superadmin: Mapped[bool] = mapped_column(Boolean, default=False)  # Permissão para criar super administradores
    can_remove_user: Mapped[bool] = mapped_column(Boolean, default=False)      # Permissão para remover usuários
    can_remove_admins: Mapped[bool] = mapped_column(Boolean, default=False)    # Permissão para remover administradores
    can_edit_roles: Mapped[bool] = mapped_column(Boolean, default=False)       # Permissão para editar funções de usuários
    can_view_user_slideshows: Mapped[bool] = mapped_column(Boolean, default=False)  # Permissão para visualizar slideshows de usuários
    can_remove_user_from_slideshow: Mapped[bool] = mapped_column(Boolean, default=False)  # Permissão para remover usuários de slideshows

    # Meu Perfil
    can_edit_own_profile: Mapped[bool] = mapped_column(Boolean, default=True)  # Permissão para editar o próprio perfil

    # Carrossel
    can_view_carousel: Mapped[bool] = mapped_column(Boolean, default=True)    # Permissão para visualizar o carrossel de mídias

    role: Mapped[Role] = relationship(
        back_populates="permissions"
    )
