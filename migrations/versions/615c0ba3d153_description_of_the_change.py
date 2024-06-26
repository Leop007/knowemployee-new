"""description of the change

Revision ID: 615c0ba3d153
Revises: 79b85c434622
Create Date: 2023-10-15 12:15:11.481828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '615c0ba3d153'
down_revision = '79b85c434622'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('testing_result', schema=None) as batch_op:
        batch_op.add_column(sa.Column('only', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('multiple', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('username_bool', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('username', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('testing_result', schema=None) as batch_op:
        batch_op.drop_column('username')
        batch_op.drop_column('username_bool')
        batch_op.drop_column('multiple')
        batch_op.drop_column('only')

    # ### end Alembic commands ###
