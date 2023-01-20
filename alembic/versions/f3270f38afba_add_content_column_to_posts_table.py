"""add content column to posts table

Revision ID: f3270f38afba
Revises: ff6012712f9b
Create Date: 2023-01-19 19:28:20.348623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3270f38afba'
down_revision = 'ff6012712f9b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String,nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
