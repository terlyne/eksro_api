"""update feedback table

Revision ID: 71d6ba3fd633
Revises: aa044440a26b
Create Date: 2025-10-08 20:01:35.009481

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "71d6ba3fd633"
down_revision: Union[str, Sequence[str], None] = "aa044440a26b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "feedbacks", "phone", existing_type=sa.VARCHAR(length=30), nullable=True
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "feedbacks", "phone", existing_type=sa.VARCHAR(length=30), nullable=False
    )
