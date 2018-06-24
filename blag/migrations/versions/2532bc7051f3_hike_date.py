"""Make hike datetime a date

Revision ID: 2532bc7051f3
Revises: f1d3540eda1e
Create Date: 2017-03-08 08:37:16.163197

"""

# revision identifiers, used by Alembic.
revision = '2532bc7051f3'
down_revision = 'f1d3540eda1e'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hike', sa.Column('created_at', sa.DateTime(), server_default=sa.text(u'now()'), nullable=False))
    op.add_column('hike', sa.Column('date', sa.Date(), server_default=sa.text(u'now()'), nullable=False))
    op.drop_column('hike', 'datetime')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hike', sa.Column('datetime', postgresql.TIMESTAMP(), server_default=sa.text(u'now()'), autoincrement=False, nullable=False))
    op.drop_column('hike', 'date')
    op.drop_column('hike', 'created_at')
    ### end Alembic commands ###