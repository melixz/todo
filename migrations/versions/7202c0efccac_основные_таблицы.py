"""основные таблицы

Revision ID: 7202c0efccac
Revises:
Create Date: 2025-08-20 00:37:46.625869

"""

from typing import Sequence, Union



# revision identifiers, used by Alembic.
revision: str = "7202c0efccac"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
