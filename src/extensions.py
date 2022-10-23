from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.ext.declarative import declarative_base
from flasgger import Swagger
from flask_smorest import Api

# jwt_manager = JWTManager()
# login_manager = LoginManager()
migrate = Migrate()
db = SQLAlchemy()
ma = Marshmallow()
# Base = declarative_base()
api = Api()
swag = Swagger()
