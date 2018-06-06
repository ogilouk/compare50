"""empty message

Revision ID: 979e89a469db
Revises: 7a57bd921158
Create Date: 2018-06-06 02:17:13.798010

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '979e89a469db'
down_revision = '7a57bd921158'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fragment')
    op.drop_table('hash')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fragment',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('hash_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('file_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('start', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('end', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['file_id'], ['file.id'], name='fragment_ibfk_1', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['hash_id'], ['hash.id'], name='fragment_ibfk_2', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_table('hash',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('pass_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['pass_id'], ['pass.id'], name='hash_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###