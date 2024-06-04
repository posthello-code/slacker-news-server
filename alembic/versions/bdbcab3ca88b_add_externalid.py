"""add externalId

Revision ID: bdbcab3ca88b
Revises: 
Create Date: 2024-05-22 21:40:16.052245

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bdbcab3ca88b"
down_revision: Union[str, None] = "a80586652854"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("sources", sa.Column("externalId", sa.Integer))


def downgrade() -> None:
    op.drop_column("sources", "externalId")
