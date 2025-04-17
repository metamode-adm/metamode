"""📦 ${message}

🔁 Revision ID: ${up_revision}
🔙 Revises: ${down_revision | comma,n}
🕓 Create Date: ${create_date}
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# ===============================
# 🔖 Identificadores da Revisão
# ===============================
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}

# ===============================
# 🚀 Função de Upgrade
# ===============================
def upgrade() -> None:
    """Aplica as mudanças no schema do banco de dados."""
    ${upgrades if upgrades else "pass"}

# ===============================
# ⏪ Função de Downgrade
# ===============================
def downgrade() -> None:
    """Desfaz as mudanças aplicadas no schema."""
    ${downgrades if downgrades else "pass"}
