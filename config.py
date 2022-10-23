import os


class Config:
    JWT_SECRET_KEY = 'SECRET' # os.environ['JWT_SECRET_KEY']
    SECRET_KEY = 'SECRET' # os.environ['SECRET_KEY']
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@localhost/purch'
    # /var/lib/postgresql/14/main/
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = Config
