from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('teachersapp.default_settings')
app.config.from_envvar('YOURAPPLICATION_SETTINGS')

db = SQLAlchemy(app)

@event.listens_for(db.engine, "connect")
def load_spatialite(dbapi_conn, connection_record):
  # From https://geoalchemy-2.readthedocs.io/en/latest/spatialite_tutorial.html
  print('enable_load_extension')
  dbapi_conn.enable_load_extension(True)
  print('load_extension')
  dbapi_conn.execute('SELECT load_extension("mod_spatialite")') 
  # originally I would try and load the extension with the line below,
  # using load_extension function, but that actually crashed my whole Flask app. 
  # doing it via a SELECT fixed that problem for me.
  #dbapi_conn.load_extension('/usr/local/lib/mod_spatialite')
  

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from teachersapp import models
from teachersapp import routes