"""empty message

Revision ID: 37907ce52504
Revises: 37164e7e3fde
Create Date: 2016-05-15 18:25:30.211477

"""

# revision identifiers, used by Alembic.
revision = '37907ce52504'
down_revision = '37164e7e3fde'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appointment', sa.Column('agent_id', sa.Integer(), nullable=True))
    op.drop_column('appointment', 'updated_at')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appointment', sa.Column('updated_at', sa.DATETIME(), nullable=True))
    op.drop_column('appointment', 'agent_id')
    ### end Alembic commands ###
