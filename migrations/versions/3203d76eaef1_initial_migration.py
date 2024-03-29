"""Initial migration.

Revision ID: 3203d76eaef1
Revises: 
Create Date: 2021-03-21 17:35:55.924283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3203d76eaef1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('languages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('user_type', sa.Enum('Admin', 'Regular', name='usertypes'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('profile_image_file', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    op.create_table('teaching_profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('service_description', sa.Text(), nullable=False),
    sa.Column('contact_details', sa.Text(), nullable=True),
    sa.Column('service_address', sa.String(length=200), nullable=False),
    # this will not work at this point because the DB doesnt have spatialite 'installed'
    #sa.Column('service_location', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, management=True, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teaching_profile_languages',
    sa.Column('left_id', sa.Integer(), nullable=True),
    sa.Column('right_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['left_id'], ['teaching_profiles.id'], ),
    sa.ForeignKeyConstraint(['right_id'], ['languages.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teaching_profile_languages')
    op.drop_table('teaching_profiles')
    op.drop_table('users')
    op.drop_table('languages')
    # ### end Alembic commands ###
