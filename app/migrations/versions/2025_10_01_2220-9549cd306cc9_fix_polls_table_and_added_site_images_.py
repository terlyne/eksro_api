"""fix polls table and added site images table

Revision ID: 9549cd306cc9
Revises: 3e5d6e880ade
Create Date: 2025-10-01 22:20:46.317564

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "9549cd306cc9"
down_revision: Union[str, Sequence[str], None] = "3e5d6e880ade"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "site_images",
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("image_url", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_site_images")),
    )

    op.drop_constraint(
        "fk_poll_answers_question_id_poll_questions", "poll_answers", type_="foreignkey"
    )

    op.drop_table("poll_questions")

    op.add_column("poll_answers", sa.Column("poll_id", sa.Uuid(), nullable=False))

    op.create_foreign_key(
        op.f("fk_poll_answers_poll_id_polls"),
        "poll_answers",
        "polls",
        ["poll_id"],
        ["id"],
    )

    op.drop_column("poll_answers", "question_id")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "poll_answers",
        sa.Column("question_id", sa.UUID(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(
        op.f("fk_poll_answers_poll_id_polls"), "poll_answers", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_poll_answers_question_id_poll_questions"),
        "poll_answers",
        "poll_questions",
        ["question_id"],
        ["id"],
    )
    op.drop_column("poll_answers", "poll_id")
    op.create_table(
        "poll_questions",
        sa.Column("question_text", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column("poll_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["poll_id"], ["polls.id"], name=op.f("fk_poll_questions_poll_id_polls")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_poll_questions")),
    )
    op.drop_table("site_images")
