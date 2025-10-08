"""add fields 'title' and 'description' to banners table

Revision ID: b43527a727a1
Revises: 5683800826f0
Create Date: 2025-10-02 16:01:29.810990

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b43527a727a1"
down_revision: Union[str, Sequence[str], None] = "5683800826f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("banners", sa.Column("title", sa.Text(), nullable=False))
    op.add_column("banners", sa.Column("description", sa.Text(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("banners", "description")
    op.drop_column("banners", "title")
