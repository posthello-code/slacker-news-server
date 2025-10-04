"""add externalUuid columns

Revision ID: b1c2d3e4f5a6
Revises: a01d8f7bb75f
Create Date: 2025-10-01 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b1c2d3e4f5a6"
down_revision: Union[str, None] = "a01d8f7bb75f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("sources", sa.Column("externalUuid", sa.String(), nullable=True))
    op.add_column("stories", sa.Column("externalUuid", sa.String(), nullable=True))
    op.create_unique_constraint("uq_sources_externalUuid", "sources", ["externalUuid"])
    op.create_unique_constraint("uq_stories_externalUuid", "stories", ["externalUuid"])


def downgrade() -> None:
    op.drop_constraint("uq_stories_externalUuid", "stories", type_="unique")
    op.drop_constraint("uq_sources_externalUuid", "sources", type_="unique")
    op.drop_column("stories", "externalUuid")
    op.drop_column("sources", "externalUuid")