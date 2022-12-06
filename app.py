from flask import Flask
import warnings

import extensions
import views
from config import config
from flask_cors import CORS
from werkzeug.routing import BaseConverter


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)
    register_extensions(app)
    api = extensions.create_api(app)
    warnings.filterwarnings(
        "ignore",
        message="Multiple schemas resolved to the name "
    )
    views.register_blueprints(api)
    return app


def register_extensions(app):
    from extensions.database import db
    from extensions.database import migrate
    migrate.init_app(app, db)


app = create_app()
