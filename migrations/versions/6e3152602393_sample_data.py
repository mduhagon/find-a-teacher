"""Sample data.

Revision ID: 6e3152602393
Revises: 77311ac03413
Create Date: 2021-03-22 08:59:00.623301

"""
from alembic import op
from sqlalchemy import Table, MetaData
from alembic import op
from datetime import date
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Date
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6e3152602393'
down_revision = '77311ac03413'
branch_labels = None
depends_on = None


def upgrade():
    meta = MetaData(bind=op.get_bind())

    #only=('users','teaching_profiles', 'languages')
    meta.reflect()

    users_table = Table('users', meta)
    profiles_table = Table('teaching_profiles', meta)
    languages_table = Table('languages', meta)
    teaching_profile_languages_table = Table('teaching_profile_languages', meta)

    # Insert available languages
    op.bulk_insert(languages_table,
        [
            {'id': 1, 'name': "English"},
            {'id': 2, 'name': "Spanish"},
            {'id': 3, 'name': "French"},
            {'id': 4, 'name': "Japanese"},
            {'id': 5, 'name': "German"},
            {'id': 6, 'name': "Russian"},
            {'id': 7, 'name': "Chinese"},
            {'id': 8, 'name': "Italian"},
            {'id': 9, 'name': "Portuguese"},
            {'id': 10, 'name': "Arabic"},
            {'id': 11, 'name': "Korean"},
            {'id': 12, 'name': "Ukrainian"},
            {'id': 13, 'name': "Polish"},
            {'id': 14, 'name': "Greek"},
            {'id': 15, 'name': "Serbian"},
            {'id': 16, 'name': "Hebrew"},
            {'id': 17, 'name': "Dutch"},
            {'id': 18, 'name': "Danish"},
            {'id': 19, 'name': "Urdu"},
            {'id': 20, 'name': "Norwegian"},
            {'id': 21, 'name': "Czech"},
            {'id': 22, 'name': "Swedish"},
            {'id': 23, 'name': "Khmer"},
            {'id': 24, 'name': "Belarusian"},
            {'id': 25, 'name': "Sanskrit"},
            {'id': 26, 'name': "Tibetan"},
            {'id': 27, 'name': "Lithuanian"},
            {'id': 28, 'name': "Slovak"},
            {'id': 29, 'name': "Vietnamese"},
            {'id': 30, 'name': "Telugu"},
            {'id': 31, 'name': "Tamil"},
            {'id': 32, 'name': "Sign"},
            {'id': 33, 'name': "Tagalog"},
            {'id': 34, 'name': "Romanian"},
            {'id': 35, 'name': "Irish"},
            {'id': 36, 'name': "Icelandic"},
            {'id': 37, 'name': "Farsi"},
            {'id': 38, 'name': "Croatian"},
            {'id': 39, 'name': "Catalan"},
            {'id': 40, 'name': "Bulgarian"},
            {'id': 41, 'name': "Bengali"},
            {'id': 42, 'name': "Indonesian"},
            {'id': 43, 'name': "Turkish"},
            {'id': 44, 'name': "Finnish"},
            {'id': 45, 'name': "Thai"},
            {'id': 46, 'name': "Hungarian"},
            {'id': 47, 'name': "Latin"},
            {'id': 48, 'name': "Punjabi"},
            {'id': 49, 'name': "Hindi"}
        ]
    )

    # Insert admin user
    op.bulk_insert(users_table,
        [
            {
                'id': 1, 
                'name': "admin", 
                'email': "admin@sample.com", 
                'password': "$2b$12$1Jt/cDK0NvMtehHXIpjzKeC17RcuwXBbO0A6yF8QoT2aJRaV0Tn7C", 
                'user_type': "Admin",
                'created_at': op.inline_literal("2021-01-01 00:00:00"),
                'profile_image_file': "default.jpeg"
            }
        ],
        multiinsert=False
    )        

    # Insert sample profiles
    op.bulk_insert(users_table,
        [
            {
                'id': 2, 
                'name': "johnDoe", 
                'email': "john.doe@sample.com", 
                'password': "$2b$12$1Jt/cDK0NvMtehHXIpjzKeC17RcuwXBbO0A6yF8QoT2aJRaV0Tn7C", 
                'user_type': "Regular",
                'created_at': op.inline_literal("2021-01-01 00:00:00"),
                'profile_image_file': "default.jpeg"
            },
            {
                'id': 3, 
                'name': "janeDoe", 
                'email': "jane.doe@sample.com", 
                'password': "$2b$12$1Jt/cDK0NvMtehHXIpjzKeC17RcuwXBbO0A6yF8QoT2aJRaV0Tn7C", 
                'user_type': "Regular",
                'created_at': op.inline_literal("2021-01-01 00:00:00"),
                'profile_image_file': "default.jpeg"
            }
        ],
        multiinsert=False
    )
    op.bulk_insert(profiles_table,
        [
            {
                'id': 1, 
                'user_id': 2,
                'title': 'Hello, I am John, and I could be your English teacher',
                'service_description': 'Hello! I am John, I adapt my classes to beginners or advanced students, I am open to any questions you may have!',
                'contact_details': "", 
                'service_address': "Sprengelstraße 26, 13353 Berlin, Germany", 
                'date_posted': op.inline_literal("2021-01-01 00:00:00")
            },
            {
                'id': 2, 
                'user_id': 3,
                'title': 'Hello, I am Jane, and I could be your German teacher',
                'service_description': 'Hello! I am Jane, I adapt my classes to beginners or advanced students, I am open to any questions you may have!',
                'contact_details': "", 
                'service_address': "Unter den Linden 42, 10117 Berlin, Germany", 
                'date_posted': op.inline_literal("2021-01-01 00:00:00")
            }
        ],
        multiinsert=False
    )      

    # The location column is special, we know how to set its value using function
    # GeomFromEWKT only, and did not found a way to call that from bulk_insert (it would be treated as string)
    # op.execute allows us to pass direct SQL we want, so we can use that: 
    op.execute("UPDATE teaching_profiles SET service_location = GeomFromEWKT('SRID=4326;POINT(13.35204 52.541032)') WHERE id = 1;")
    op.execute("UPDATE teaching_profiles SET service_location = GeomFromEWKT('SRID=4326;POINT(13.385914 52.517434)') WHERE id = 2;")

    # Set which language each of my teachers teaches:
    op.bulk_insert(teaching_profile_languages_table,
        [
            {'left_id': 1, 'right_id': 1}, # 1 is English
            {'left_id': 2, 'right_id': 5} # 5 is German
        ]
    )        


def downgrade():
    # The order of the operations is important, otherwise constraints would fail
    op.execute("DELETE FROM teaching_profile_languages WHERE 1 = 1;")
    op.execute("DELETE FROM teaching_profiles WHERE 1 = 1;")
    op.execute("DELETE FROM users WHERE 1 = 1;")
    op.execute("DELETE FROM languages WHERE 1 = 1;")
