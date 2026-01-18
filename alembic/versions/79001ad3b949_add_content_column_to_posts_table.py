"""add content column to posts table

Revision ID: 79001ad3b949
Revises: 187ed2bf713e
Create Date: 2026-01-17 16:32:26.784015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79001ad3b949'
down_revision: Union[str, Sequence[str], None] = '187ed2bf713e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False) )
    pass


def downgrade() -> None:    #UNDO the column that has been created
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
