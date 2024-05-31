"""add externalId columns

Revision ID: fc766bf2e128
Revises: fd8dcdf0be96
Create Date: 2024-05-30 23:25:02.974197

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fc766bf2e128"
down_revision: Union[str, None] = "fd8dcdf0be96"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("comments", sa.Column("externalId", sa.Integer))
    op.add_column("stories", sa.Column("externalId", sa.Integer))


def downgrade() -> None:
    op.drop_column("comments", "externalId")
    op.drop_column("stories", "externalId")
