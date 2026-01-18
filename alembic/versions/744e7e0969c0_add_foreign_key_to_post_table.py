"""add foreign-key to post table

Revision ID: 744e7e0969c0
Revises: a765316e6ccb
Create Date: 2026-01-17 17:57:02.593969

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '744e7e0969c0'
down_revision: Union[str, Sequence[str], None] = 'a765316e6ccb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users",local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
