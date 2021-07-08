"""add-bike-kayak

Revision ID: f9012dfdf7e4
Revises: a675e757e11f
Create Date: 2021-07-08 19:58:20.021000

"""

# revision identifiers, used by Alembic.
revision = 'f9012dfdf7e4'
down_revision = 'a675e757e11f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_check_constraint(
        'hike_method_check2',
        'hike',
        "method in ('ski', 'foot', 'crampons', 'climb', 'via ferrata', 'bike', 'kayak')"
    )
    op.drop_constraint('hike_method_check', 'hike')


def downgrade():
    op.create_check_constraint(
        'hike_method_check',
        'hike',
        "method in ('ski', 'foot', 'crampons', 'climb', 'via ferrata')"
    )
    op.drop_constraint('hike_method_check2', 'hike')
