import os


class Config:
    JWT_SECRET_KEY = 'SECRET' # os.environ['JWT_SECRET_KEY']
    SECRET_KEY = 'SECRET' # os.environ['SECRET_KEY']
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@localhost/purch'
    # /var/lib/postgresql/14/main/
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    API_TITLE = 'PURCH.io'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/'

    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/"

    API_SPEC_OPTIONS = {
        'info': {'description': 'This is an API for the purch.io purchasing app.',
                 'termsOfService': 'http://helloreverb.com/terms/',
                 'contact': {
                     'email': 'test@swagger.io'
                 },
                 'license': {
                     'name': 'MIT License',
                     'url': 'https://fr.wikipedia.org/wiki/Licence_MIT'
                 }
                 }
    }


config = Config
