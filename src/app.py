from flask import Flask
from config import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    from extensions import db
    from extensions import jwt_manager
    # from extensions import login_manager
    from extensions import migrate
    from extensions import ma
    ma.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    jwt_manager.init_app(app)
    # login_manager.init_app(app)
    # login_manager.login_view = 'webapp.login'


def register_blueprints(app):
    from api import api_bp
    # from webapp import webapp_bp

    app.register_blueprint(api_bp)
    # app.register_blueprint(webapp_bp)


app = create_app()
