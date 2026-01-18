"""create posts table

Revision ID: 187ed2bf713e
Revises: 
Create Date: 2026-01-17 14:12:47.730292

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '187ed2bf713e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:    #run commands for making changes that you want to do.Handles the changes to table
    """Upgrade schema."""
    op.create_table('posts',sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title',sa.String(),nullable=False))
    
    pass


def downgrade() -> None:    #if u want to delete teh updated table put all logic of upgrade into downgrade to handle removing the table.Handles rolling it back   UNDO THE UPGRADE PROCESS
    """Downgrade schema."""
    op.drop_table('posts')
    
    pass
