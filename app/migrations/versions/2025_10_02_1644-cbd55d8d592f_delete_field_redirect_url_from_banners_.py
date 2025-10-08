"""delete field 'redirect_url' from banners table

Revision ID: cbd55d8d592f
Revises: b43527a727a1
Create Date: 2025-10-02 16:44:16.422996

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cbd55d8d592f"
down_revision: Union[str, Sequence[str], None] = "b43527a727a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("banners", "redirect_url")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "banners",
        sa.Column("redirect_url", sa.TEXT(), autoincrement=False, nullable=False),
    )
