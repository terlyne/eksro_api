"""change feedback table

Revision ID: aa044440a26b
Revises: cbd55d8d592f
Create Date: 2025-10-08 19:47:18.754453

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aa044440a26b"
down_revision: Union[str, Sequence[str], None] = "cbd55d8d592f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("feedbacks", sa.Column("name", sa.Text(), nullable=False))
    op.add_column("feedbacks", sa.Column("phone", sa.String(length=30), nullable=False))
    op.drop_column("feedbacks", "first_name")
    op.drop_column("feedbacks", "middle_name")
    op.drop_column("feedbacks", "last_name")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "feedbacks",
        sa.Column("last_name", sa.TEXT(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "feedbacks",
        sa.Column("middle_name", sa.TEXT(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "feedbacks",
        sa.Column("first_name", sa.TEXT(), autoincrement=False, nullable=False),
    )
    op.drop_column("feedbacks", "phone")
    op.drop_column("feedbacks", "name")
