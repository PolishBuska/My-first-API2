"""add last columns to our posts table

Revision ID: 4ce9d76c8166
Revises: 4a43597e6650
Create Date: 2023-01-19 20:12:40.705749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ce9d76c8166'
down_revision = '4a43597e6650'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published',
        sa.Boolean(),
        nullable = False,
        server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at',
        sa.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sa.text('NOW()')

    ))

    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts','published')
    pass
