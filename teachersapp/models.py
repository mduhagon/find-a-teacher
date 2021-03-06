import enum
from datetime import datetime
from teachersapp import db, login_manager
from flask_login import UserMixin
from sqlalchemy import func
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKTElement
import json


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class UserTypes(enum.Enum):
   Admin = 1
   Regular = 2

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.Enum(UserTypes), nullable=False, default=UserTypes.Regular)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    profile_image_file = db.Column(db.String(120), nullable=False, default='default.jpeg')

    teaching_profiles = db.relationship('TeachingProfile', back_populates='user', order_by="TeachingProfile.id", lazy=True)
    
    def __repr__(self):
        return f"User({self.id}, '{self.name}', '{self.email}', type:{self.user_type})"        

# To be able to model a many to many relationship between TeachingProfiles and Languages
# I need to model the association table.
# (a teaching profile can offer multiple languages and each language in the platform is
#  offered by multiple teachers)
profile_languages_table = db.Table('teaching_profile_languages', db.Model.metadata,
    db.Column('left_id', db.Integer, db.ForeignKey('teaching_profiles.id')),
    db.Column('right_id', db.Integer, db.ForeignKey('languages.id'))
)

class SpatialConstants:
    # SRID stands for Spatial Reference ID, some explanation of why we need one here: 
    # https://www.gaia-gis.it/gaia-sins/spatialite-cookbook/html/srid.html
    SRID = 4326

class TeachingProfile(db.Model): 
    __tablename__ = 'teaching_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    service_description = db.Column(db.Text, nullable=False)
    contact_details = db.Column(db.Text)
    service_address = db.Column(db.String(200), nullable=False)
    service_location = db.Column(Geometry("POINT", srid=SpatialConstants.SRID, dimension=2, management=True)) 
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # many to one side of the relationship of TeachingProfiles with Users
    user = db.relationship("User", back_populates="teaching_profiles")
    
    offered_languages = db.relationship(
        "Language",
        secondary=profile_languages_table,
        back_populates="teaching_offers"
    )

    # This is a convenience method to display all
    # languages offered in a string like:
    # Language 1 / Language 2 / Language 3
    def offered_languages_str(self):
        return ' / '.join([str(elem.name) for elem in self.offered_languages])

    def get_service_location_latitude(self):
        point = to_shape(self.service_location)
        return point.y

    def get_service_location_longitude(self):
        point = to_shape(self.service_location)
        return point.x  

    def __repr__(self):
        return f"TeachingProfile({self.id}, user_id: {self.user_id}, '{self.title}')"

    # This can probably be improved. The aim of this method
    # is to provide a serializable representation of an instance of
    # this class, to be converted to json and return by the api routes
    def toDict(self):
        return {
            'id': self.id,
            'user_name': self.user.name,
            'title': self.title,
            'address': self.service_address,
            'location': {
                'lng': self.get_service_location_longitude(),
                'lat': self.get_service_location_latitude()
            },
            'description': self.service_description,
            'languages': self.offered_languages_str()
        }    

    @staticmethod
    def get_profiles_within_radius(lat, lng, radius):
        """Return all teaching profiles within a given radius (in meters)"""
        return TeachingProfile.query.filter(
            func.PtDistWithin(
                TeachingProfile.service_location, 
                func.MakePoint(lng, lat, SpatialConstants.SRID), 
                radius)
            ).limit(100).all() #TODO: do I need to limit?

    @staticmethod
    def point_representation(latitude, longitude):
        point = 'POINT(%s %s)' % (longitude, latitude)
        wkb_element = WKTElement(point, srid=SpatialConstants.SRID)
        return wkb_element


class Language(db.Model):   
    __tablename__ = 'languages'  

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    teaching_offers = db.relationship(
        "TeachingProfile", 
        secondary=profile_languages_table,
        back_populates="offered_languages"
    )

    def __repr__(self):
        return f"Language({self.id}, '{self.name}')"
