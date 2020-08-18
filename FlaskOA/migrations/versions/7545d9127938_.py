"""empty message

Revision ID: 7545d9127938
Revises: 
Create Date: 2020-08-17 19:27:20.407491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7545d9127938'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('department',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('news',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=32), nullable=True),
    sa.Column('author', sa.String(length=32), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('public_time', sa.Date(), nullable=True),
    sa.Column('picture', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('permission',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('desc', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('position',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['department.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('permission_position',
    sa.Column('position.id', sa.Integer(), nullable=True),
    sa.Column('permission.id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['permission.id'], ['permission.id'], ),
    sa.ForeignKeyConstraint(['position.id'], ['position.id'], )
    )
    op.create_table('person',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('nickname', sa.String(length=32), nullable=True),
    sa.Column('gender', sa.String(length=32), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('jobnum', sa.String(length=32), nullable=False),
    sa.Column('phone', sa.String(length=32), nullable=True),
    sa.Column('email', sa.String(length=32), nullable=True),
    sa.Column('photo', sa.String(length=64), nullable=True),
    sa.Column('address', sa.String(length=128), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('position_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['position_id'], ['position.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('jobnum')
    )
    op.create_table('attendance',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('reason', sa.Text(), nullable=True),
    sa.Column('atype', sa.String(length=32), nullable=True),
    sa.Column('adate', sa.Float(), nullable=True),
    sa.Column('start_time', sa.Date(), nullable=True),
    sa.Column('end_time', sa.Date(), nullable=True),
    sa.Column('examine', sa.String(length=32), nullable=True),
    sa.Column('astatue', sa.String(length=32), nullable=True),
    sa.Column('person_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attendance')
    op.drop_table('person')
    op.drop_table('permission_position')
    op.drop_table('position')
    op.drop_table('permission')
    op.drop_table('news')
    op.drop_table('department')
    # ### end Alembic commands ###