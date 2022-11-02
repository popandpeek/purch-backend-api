from . import database
from .api import Api


def create_api(app):
    new_api = Api(app)
    database.init_app(app)
    return new_api
