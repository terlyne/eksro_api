"""change news table, delete body field and add news_url field

Revision ID: a547e6b9f2ec
Revises: 9549cd306cc9
Create Date: 2025-10-01 23:02:31.226686

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a547e6b9f2ec"
down_revision: Union[str, Sequence[str], None] = "9549cd306cc9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("news", sa.Column("news_url", sa.Text(), nullable=False))
    op.drop_column("news", "body")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "news", sa.Column("body", sa.TEXT(), autoincrement=False, nullable=False)
    )
    op.drop_column("news", "news_url")
