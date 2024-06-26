"""empty message

Revision ID: 7de4e959b8eb
Revises: 9ad2f68587fb
Create Date: 2024-06-08 21:49:27.976767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7de4e959b8eb'
down_revision = '9ad2f68587fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('username', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite__planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id_favorites', sa.Integer(), nullable=True),
    sa.Column('favorite_planet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['favorite_planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id_favorites'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite__people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id_favorites', sa.Integer(), nullable=True),
    sa.Column('favorite_person_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['favorite_person_id'], ['person.id'], ),
    sa.ForeignKeyConstraint(['user_id_favorites'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite__people')
    op.drop_table('favorite__planets')
    op.drop_table('users')
    # ### end Alembic commands ###
