"""make externalIds unique for comments

Revision ID: a01d8f7bb75f
Revises: fc766bf2e128
Create Date: 2024-06-01 09:46:17.381880

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a01d8f7bb75f"
down_revision: Union[str, None] = "fc766bf2e128"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("externalId", "comments", ["externalId"])


def downgrade() -> None:
    op.drop_constraint("externalId", "comments")
