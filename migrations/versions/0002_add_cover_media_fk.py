"""🔗 Add FK cover_media_id on slideshows

🔁 Revision ID: 0002_add_cover_media_fk
🔙 Revises: 72d8d76c9ea8
🕓 Create Date: 2025-04-06 01:10:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '0002_add_cover_media_fk'
down_revision: Union[str, None] = '72d8d76c9ea8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Adiciona a foreign key cover_media_id após criação das tabelas."""
    op.create_foreign_key(
        "fk_slideshows_cover_media_id",
        "slideshows", "media",
        ["cover_media_id"], ["id"]
    )

def downgrade() -> None:
    """Remove a foreign key cover_media_id."""
    op.drop_constraint(
        "fk_slideshows_cover_media_id",
        "slideshows",
        type_="foreignkey"
    )
