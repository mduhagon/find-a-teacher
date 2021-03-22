"""Spatialite tables.

Revision ID: 77311ac03413
Revises: 3203d76eaef1
Create Date: 2021-03-22 08:25:34.644359

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKTElement

# revision identifiers, used by Alembic.
revision = '77311ac03413'
down_revision = '3203d76eaef1'
branch_labels = None
depends_on = None


def upgrade():
    # This will create a bunch of tables that Spatialite needs
    # to run properly.
    op.execute("SELECT InitSpatialMetaData();")

    op.execute("SELECT load_extension(\"mod_spatialite\");")
    
    # Now that Spatialite is 'installed' we can use it
    # to create the location column on teaching_profiles
    op.execute("SELECT AddGeometryColumn('teaching_profiles', 'service_location', 4326, 'POINT', 'XY');")
 
    #op.add_column('teaching_profiles', sa.Column('service_location', Geometry(geometry_type='POINT', srid=4326, management=True, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True))


def downgrade():
    # From Spatialite documentation: https://www.gaia-gis.it/gaia-sins/spatialite-cookbook-5/cookbook_topics.adminstration.html
    # Spatialite does allow you to revert what it created with AddGeometryColumn or RecoverGeometryColumn commands
    # With the DiscardGeometryColumn command, the entries in the geometry_columns TABLE and the created TRIGGERs will be removed,
    # but the column 'geom_city', with its data in the 'admin_cities' TABLE will still exist. 
    # This in turn is because SQLite itself does not support dropping columns.
    # We will do our best here and discard the geometry column, which will do partial cleanup but
    # Not a real full downgrade
    op.execute("SELECT DiscardGeometryColumn('teaching_profiles', 'service_location');")

    op.drop_index('idx_viewsjoin', table_name='views_geometry_columns')
    op.drop_table('views_geometry_columns')
    op.drop_table('spatialite_history')
    op.drop_table('idx_teaching_profiles_service_location_node')
    op.drop_table('geometry_columns_statistics')
    op.drop_table('geometry_columns_time')
    op.drop_table('virts_geometry_columns_statistics')
    op.drop_table('data_licenses')
    op.drop_table('geometry_columns_field_infos')
    op.drop_table('virts_geometry_columns_auth')
    op.drop_table('views_geometry_columns_field_infos')
    op.drop_table('KNN')
    op.drop_table('ElementaryGeometries')
    op.drop_table('idx_teaching_profiles_service_location_rowid')
    op.drop_table('SpatialIndex')
    op.drop_table('views_geometry_columns_statistics')
    op.drop_table('virts_geometry_columns_field_infos')
    op.drop_table('geometry_columns_auth')
    op.drop_table('spatial_ref_sys_aux')
    op.drop_table('views_geometry_columns_auth')
    op.drop_index('idx_spatial_ref_sys', table_name='spatial_ref_sys')
    op.drop_table('spatial_ref_sys')
    op.drop_index('idx_virtssrid', table_name='virts_geometry_columns')
    op.drop_table('virts_geometry_columns')
    op.drop_table('sql_statements_log')
    op.drop_index('idx_srid_geocols', table_name='geometry_columns')
    op.drop_table('geometry_columns')
    op.drop_table('idx_teaching_profiles_service_location')
    op.drop_table('idx_teaching_profiles_service_location_parent')