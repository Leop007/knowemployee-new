"""description of the change

Revision ID: 5a76264685dc
Revises: fd48a957430c
Create Date: 2023-10-12 18:23:14.059738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a76264685dc'
down_revision = 'fd48a957430c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('testing_result', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('testing_result', schema=None) as batch_op:
        batch_op.drop_column('type')

    # ### end Alembic commands ###