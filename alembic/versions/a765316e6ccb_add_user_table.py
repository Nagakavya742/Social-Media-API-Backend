"""add user table

Revision ID: a765316e6ccb
Revises: 79001ad3b949
Create Date: 2026-01-17 17:05:12.001639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a765316e6ccb'
down_revision: Union[str, Sequence[str], None] = '79001ad3b949'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
                    sa.Column('id',sa.INTEGER(),nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')                    
                    )
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
