"""change projects table. delete 'body' field and add 'project_url' field

Revision ID: 5683800826f0
Revises: a547e6b9f2ec
Create Date: 2025-10-01 23:30:23.351812

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5683800826f0"
down_revision: Union[str, Sequence[str], None] = "a547e6b9f2ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("projects", sa.Column("project_url", sa.Text(), nullable=False))
    op.drop_column("projects", "body")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "projects", sa.Column("body", sa.TEXT(), autoincrement=False, nullable=False)
    )
    op.drop_column("projects", "project_url")
