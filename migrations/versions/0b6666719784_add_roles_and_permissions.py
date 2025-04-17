"""📦 add roles and permissions

🔁 Revision ID: 0b6666719784
🔙 Revises: 0002_add_cover_media_fk
🕓 Create Date: 2025-04-08 21:40:39.058178
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# ===============================
# 🔖 Identificadores da Revisão
# ===============================
revision: str = '0b6666719784'
down_revision: Union[str, None] = '0002_add_cover_media_fk'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# ===============================
# 🚀 Função de Upgrade
# ===============================
def upgrade() -> None:
    """Aplica as mudanças no schema do banco de dados."""
    # Criando a tabela 'roles'
    op.create_table('roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Criando a tabela 'permissions' com todas as permissões, incluindo as novas
    op.create_table('permissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('can_view_slideshow', sa.Boolean(), nullable=False),
        sa.Column('can_create_slideshow', sa.Boolean(), nullable=False),
        sa.Column('can_edit_slideshow', sa.Boolean(), nullable=False),
        sa.Column('can_view_sharing', sa.Boolean(), nullable=False),
        sa.Column('can_add_users_to_slideshow', sa.Boolean(), nullable=False),
        sa.Column('can_view_media', sa.Boolean(), nullable=False),
        sa.Column('can_upload_media', sa.Boolean(), nullable=False),
        sa.Column('can_delete_media', sa.Boolean(), nullable=False),
        sa.Column('can_reorder_media', sa.Boolean(), nullable=False),
        sa.Column('can_set_cover', sa.Boolean(), nullable=False),
        sa.Column('can_create_user', sa.Boolean(), nullable=False),
        sa.Column('can_create_superadmin', sa.Boolean(), nullable=False),
        sa.Column('can_remove_user', sa.Boolean(), nullable=False),
        sa.Column('can_remove_admins', sa.Boolean(), nullable=False),
        sa.Column('can_edit_roles', sa.Boolean(), nullable=False),
        sa.Column('can_view_user_slideshows', sa.Boolean(), nullable=False),
        sa.Column('can_remove_user_from_slideshow', sa.Boolean(), nullable=False),
        sa.Column('can_edit_own_profile', sa.Boolean(), nullable=False),
        sa.Column('can_view_carousel', sa.Boolean(), nullable=False),
        sa.Column('can_share_slideshow', sa.Boolean(), nullable=False, server_default=sa.text('false')),  # Nova permissão
        sa.Column('can_search_users', sa.Boolean(), nullable=False, server_default=sa.text('false')),  # Nova permissão
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('role_id')
    )

    # Criando a coluna 'role_id' na tabela 'users' e associando com a tabela 'roles'
    op.add_column('users', sa.Column('role_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'users', 'roles', ['role_id'], ['id'])

    # Removendo as colunas antigas de superadmin e admin
    op.drop_column('users', 'is_admin')
    op.drop_column('users', 'is_super_admin')

# ===============================
# ⏪ Função de Downgrade
# ===============================
def downgrade() -> None:
    """Desfaz as mudanças aplicadas no schema."""
    # Adicionando as colunas antigas de admin e superadmin
    op.add_column('users', sa.Column('is_super_admin', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('is_admin', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))

    # Removendo as permissões adicionadas
    op.drop_column('permissions', 'can_share_slideshow')
    op.drop_column('permissions', 'can_search_users')

    # Removendo a chave estrangeira e coluna 'role_id'
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'role_id')

    # Removendo as tabelas 'permissions' e 'roles'
    op.drop_table('permissions')
    op.drop_table('roles')
