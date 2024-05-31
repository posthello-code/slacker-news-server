"""create comment table

Revision ID: fd8dcdf0be96
Revises: bdbcab3ca88b
Create Date: 2024-05-30 19:43:19.987993

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from models.data_models import Comment


# revision identifiers, used by Alembic.
revision: str = "fd8dcdf0be96"
down_revision: Union[str, None] = "bdbcab3ca88b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "comments",
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
    )


def downgrade() -> None:
    op.drop_table("comments")
