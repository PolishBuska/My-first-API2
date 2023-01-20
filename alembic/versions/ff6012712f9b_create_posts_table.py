"""create posts table

Revision ID: ff6012712f9b
Revises: 
Create Date: 2023-01-19 19:16:31.455957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff6012712f9b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id', sa.Integer(), nullable = False,primary_key = True),
                    sa.Column('title',sa.String(), nullable = False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
