from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.event import listen
from sqlalchemy.pool import Pool
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from teachersapp.config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'

# This format will not work once you moe your app to be created with the create_app factory:
#@event.listens_for(db.engine, "connect")
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
  
from teachersapp import models

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  db.init_app(app)
  migrate.init_app(app, db)
  # alternative for @event.listens_for(db.engine, "connect")
  listen(Pool, 'connect', load_spatialite)

  bcrypt.init_app(app)
  login_manager.init_app(app)

  from teachersapp.main.routes import main
  from teachersapp.admin.routes import admin
  from teachersapp.api.routes import api
  app.register_blueprint(main)
  app.register_blueprint(admin)
  app.register_blueprint(api)

  return app
