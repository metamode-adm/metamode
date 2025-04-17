"""📦 initial migration

🔁 Revision ID: 72d8d76c9ea8
🔙 Revises: 
🕓 Create Date: 2025-04-06 00:54:14.883078
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# ===============================
# 🔖 Identificadores da Revisão
# ===============================
revision: str = '72d8d76c9ea8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# ===============================
# 🚀 Função de Upgrade
# ===============================
def upgrade() -> None:
    """Aplica as mudanças no schema do banco de dados."""

    op.create_table('slideshows',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=True),
        sa.Column('cover_media_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table('media',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('filepath', sa.String(length=500), nullable=False),
        sa.Column('file_hash', sa.String(length=64), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('size_mb', sa.Float(), nullable=False),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('slideshow_id', sa.Integer(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['slideshow_id'], ['slideshows.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('users',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=50), nullable=False),
        sa.Column('hashed_password', sa.String(length=1024), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_admin', sa.Boolean(), nullable=False),
        sa.Column('is_super_admin', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    op.create_table('user_slideshow_access',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('slideshow_id', sa.Integer(), nullable=False),
        sa.Column('can_edit', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['slideshow_id'], ['slideshows.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

# ===============================
# ⏪ Função de Downgrade
# ===============================
def downgrade() -> None:
    """Desfaz as mudanças aplicadas no schema."""
    op.drop_table('user_slideshow_access')
    op.drop_table('users')
    op.drop_table('media')
    op.drop_table('slideshows')
