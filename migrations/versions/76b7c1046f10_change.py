"""change

Revision ID: 76b7c1046f10
Revises: 02b5cbc4cf67
Create Date: 2023-11-12 18:07:04.547895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76b7c1046f10'
down_revision = '02b5cbc4cf67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quiz_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quiz_token', sa.Text(), nullable=True),
    sa.Column('token_results', sa.Text(), nullable=True),
    sa.Column('username', sa.Text(), nullable=True),
    sa.Column('answer', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quiz_results')
    # ### end Alembic commands ###