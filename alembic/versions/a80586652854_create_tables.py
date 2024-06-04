"""create tables

Revision ID: a80586652854
Revises: a01d8f7bb75f
Create Date: 2024-06-03 21:06:07.702844

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a80586652854"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "stories",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "createdDate", sa.DateTime, unique=False, server_default=sa.text("NOW()")
        ),
        sa.Column("sourceId", sa.UUID, unique=False),
        sa.Column("summary", sa.Text, unique=False),
        sa.Column("title", sa.String, unique=False),
        sa.Column("sourceUri", sa.String, unique=False),
    )
    op.create_table(
        "sources",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "createdDate", sa.DateTime, unique=False, server_default=sa.text("NOW()")
        ),
        sa.Column("sourceMethod", sa.String, unique=False),
        sa.Column("source", sa.String, unique=False),
        sa.Column("dataFormat", sa.String, unique=False),
        sa.Column("sourceUri", sa.String, unique=False),
        sa.Column("content", sa.Text, unique=False),
    )


def downgrade() -> None:
    pass
