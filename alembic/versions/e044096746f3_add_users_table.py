"""add users table

Revision ID: e044096746f3
Revises: f3270f38afba
Create Date: 2023-01-19 19:39:17.483032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e044096746f3'
down_revision = 'f3270f38afba'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable= False),
                    sa.Column('email',sa.String(), nullable = False),
                    sa.Column('password',sa.String(),nullable = False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default = sa.text('now()'),nullable = False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
