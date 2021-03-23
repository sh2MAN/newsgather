"""0002_News_pubdate

Revision ID: 4848a7d55a11
Revises: f6528aaad7ef
Create Date: 2021-03-23 20:49:01.092430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4848a7d55a11'
down_revision = 'f6528aaad7ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('news', sa.Column('pub_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('news', 'pub_date')
    # ### end Alembic commands ###