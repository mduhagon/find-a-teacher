import enum
from datetime import datetime
from teachersapp import db, login_manager
from flask_login import UserMixin


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

class TeachingProfile(db.Model): 
    __tablename__ = 'teaching_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    service_description = db.Column(db.Text, nullable=False)
    contact_details = db.Column(db.Text)
    service_address = db.Column(db.String(200), nullable=False)
    #TODO: I will need to store the location as a coordinate as well (for map integration)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # many to one side of the relationship of TeachingProfiles with Users
    user = db.relationship("User", back_populates="teaching_profiles")
    
    offered_languages = db.relationship(
        "Language",
        secondary=profile_languages_table,
        back_populates="teaching_offers"
    )

    def __repr__(self):
        return f"TeachingProfile({self.id}, user_id: {self.user_id}, '{self.title}')"

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
