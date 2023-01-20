"""add foreing-key to posts table

Revision ID: 4a43597e6650
Revises: e044096746f3
Create Date: 2023-01-19 19:55:02.829979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a43597e6650'
down_revision = 'e044096746f3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key(
        'posts_users_fk',
        source_table="posts",
        referent_table="users",
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
    )
    pass


def downgrade():
    op.drop_constraint('posts_users_fk',
                       table_name="posts")
    op.drop_column('posts','owner_id')
    pass
