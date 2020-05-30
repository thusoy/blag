"""Increase title and slug lengths

Revision ID: a675e757e11f
Revises: bce69b840145
Create Date: 2020-05-30 16:40:36.389172

"""

# revision identifiers, used by Alembic.
revision = 'a675e757e11f'
down_revision = 'bce69b840145'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('blog_post', 'title', type_=sa.Text)
    op.alter_column('blog_post', 'slug', type_=sa.Text)


def downgrade():
    op.alter_column('blog_post', 'title', type_=sa.String(40))
    op.alter_column('blog_post', 'slug', type_=sa.String(40))
