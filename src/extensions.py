from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base


jwt_manager = JWTManager()
login_manager = LoginManager()
migrate = Migrate()
db = SQLAlchemy()
ma = Marshmallow()
Base = declarative_base()
