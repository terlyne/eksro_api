"""add contacts managers and participants tables

Revision ID: aeb62fd30c5d
Revises: 71d6ba3fd633
Create Date: 2025-10-11 16:09:34.172049

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aeb62fd30c5d"
down_revision: Union[str, Sequence[str], None] = "71d6ba3fd633"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "contacts",
        sa.Column(
            "site_section",
            sa.Enum(
                "HOME",
                "ABOUT",
                "PARENTS",
                "ORGANIZATIONS",
                "SOVIETS",
                "CONTACTS",
                "PARTNERS",
                name="sitesection_enum",
            ),
            nullable=False,
        ),
        sa.Column("subpage", sa.String(length=100), nullable=True),
        sa.Column("phone", sa.String(length=40), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("vk_group", sa.Text(), nullable=True),
        sa.Column("tg_channel", sa.Text(), nullable=True),
        sa.Column("discipline", sa.Text(), nullable=True),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("work_hours", sa.Text(), nullable=True),
        sa.Column("date_of_created", sa.Date(), nullable=True),
        sa.Column("full_name", sa.Text(), nullable=True),
        sa.Column("short_name", sa.Text(), nullable=True),
        sa.Column("organization_founder", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_contacts")),
    )
    op.create_table(
        "managers",
        sa.Column("first_name", sa.Text(), nullable=False),
        sa.Column("last_name", sa.Text(), nullable=False),
        sa.Column("patronymic", sa.Text(), nullable=False),
        sa.Column("post", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_managers")),
    )
    op.create_table(
        "participants",
        sa.Column(
            "site_section",
            sa.Enum(
                "HOME",
                "ABOUT",
                "PARENTS",
                "ORGANIZATIONS",
                "SOVIETS",
                "CONTACTS",
                "PARTNERS",
                name="sitesection_enum",
            ),
            nullable=False,
        ),
        sa.Column("subpage", sa.String(length=100), nullable=True),
        sa.Column("fisrt_name", sa.Text(), nullable=False),
        sa.Column("last_name", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_participants")),
    )
    op.add_column(
        "documents",
        sa.Column(
            "site_section",
            sa.Enum(
                "HOME",
                "ABOUT",
                "PARENTS",
                "ORGANIZATIONS",
                "SOVIETS",
                "CONTACTS",
                "PARTNERS",
                name="sitesection_enum",
            ),
            nullable=False,
        ),
    )
    op.add_column(
        "documents", sa.Column("subpage", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "events",
        sa.Column(
            "site_section",
            sa.Enum(
                "HOME",
                "ABOUT",
                "PARENTS",
                "ORGANIZATIONS",
                "SOVIETS",
                "CONTACTS",
                "PARTNERS",
                name="sitesection_enum",
            ),
            nullable=False,
        ),
    )
    op.add_column("events", sa.Column("subpage", sa.String(length=100), nullable=True))
    op.add_column(
        "feedbacks",
        sa.Column(
            "site_section",
            sa.Enum(
                "HOME",
                "ABOUT",
                "PARENTS",
                "ORGANIZATIONS",
                "SOVIETS",
                "CONTACTS",
                "PARTNERS",
                name="sitesection_enum",
            ),
            nullable=False,
        ),
    )
    op.add_column(
        "feedbacks", sa.Column("subpage", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "news",
        sa.Column(
            "site_section",
            sa.Enum(
                "HOME",
                "ABOUT",
                "PARENTS",
                "ORGANIZATIONS",
                "SOVIETS",
                "CONTACTS",
                "PARTNERS",
                name="sitesection_enum",
            ),
            nullable=False,
        ),
    )
    op.add_column("news", sa.Column("subpage", sa.String(length=100), nullable=True))
    op.add_column(
        "news_types",
        sa.Column(
            "site_section",
            sa.Enum(
                "HOME",
                "ABOUT",
                "PARENTS",
                "ORGANIZATIONS",
                "SOVIETS",
                "CONTACTS",
                "PARTNERS",
                name="sitesection_enum",
            ),
            nullable=False,
        ),
    )
    op.add_column(
        "news_types", sa.Column("subpage", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "poll_answers",
        sa.Column(
            "site_section",
            sa.Enum(
                "HOME",
                "ABOUT",
                "PARENTS",
                "ORGANIZATIONS",
                "SOVIETS",
                "CONTACTS",
                "PARTNERS",
                name="sitesection_enum",
            ),
            nullable=False,
        ),
    )
    op.add_column(
        "poll_answers", sa.Column("subpage", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "polls",
        sa.Column(
            "site_section",
            sa.Enum(
                "HOME",
                "ABOUT",
                "PARENTS",
                "ORGANIZATIONS",
                "SOVIETS",
                "CONTACTS",
                "PARTNERS",
                name="sitesection_enum",
            ),
            nullable=False,
        ),
    )
    op.add_column("polls", sa.Column("subpage", sa.String(length=100), nullable=True))
    op.add_column(
        "subscribers",
        sa.Column(
            "site_section",
            sa.Enum(
                "HOME",
                "ABOUT",
                "PARENTS",
                "ORGANIZATIONS",
                "SOVIETS",
                "CONTACTS",
                "PARTNERS",
                name="sitesection_enum",
            ),
            nullable=False,
        ),
    )
    op.add_column(
        "subscribers", sa.Column("subpage", sa.String(length=100), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("subscribers", "subpage")
    op.drop_column("subscribers", "site_section")
    op.drop_column("polls", "subpage")
    op.drop_column("polls", "site_section")
    op.drop_column("poll_answers", "subpage")
    op.drop_column("poll_answers", "site_section")
    op.drop_column("news_types", "subpage")
    op.drop_column("news_types", "site_section")
    op.drop_column("news", "subpage")
    op.drop_column("news", "site_section")
    op.drop_column("feedbacks", "subpage")
    op.drop_column("feedbacks", "site_section")
    op.drop_column("events", "subpage")
    op.drop_column("events", "site_section")
    op.drop_column("documents", "subpage")
    op.drop_column("documents", "site_section")
    op.drop_table("participants")
    op.drop_table("managers")
    op.drop_table("contacts")
