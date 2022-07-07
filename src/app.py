from flask import Flask
from config import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    from src.extensions import db
    from src.extensions import jwt_manager
    # from extensions import login_manager
    from src.extensions import migrate
    from src.extensions import ma
    ma.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    jwt_manager.init_app(app)
    # login_manager.init_app(app)
    # login_manager.login_view = 'webapp.login'


def register_blueprints(app):
    from src.api import api_bp
    from src.endpoints.blueprint_users import blueprint_users
    from src.endpoints.blueprint_vendors import blueprint_vendors
    from src.endpoints.blueprint_vendor_items import blueprint_vendor_items
    from src.endpoints.blueprint_house_items import blueprint_house_items
    from src.endpoints.blueprint_house_orders import blueprint_house_orders
    from src.endpoints.blueprint_inventories import blueprint_inventories
    from src.endpoints.blueprint_invoices import blueprint_invoices
    from src.endpoints.blueprint_vendor_orders import blueprint_vendor_orders
    # from webapp import webapp_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(blueprint_users, url_prefix="/api/v1/users")
    app.register_blueprint(blueprint_vendors, url_prefix="/api/v1/vendors")
    app.register_blueprint(blueprint_vendor_items, url_prefix="/api/v1/vendor_items")
    app.register_blueprint(blueprint_house_items, url_prefix="/api/v1/house_items")
    app.register_blueprint(blueprint_house_orders, url_prefix="/api/v1/house_orders")
    app.register_blueprint(blueprint_inventories, url_prefix="/api/v1/inventories")
    app.register_blueprint(blueprint_invoices, url_prefix="/api/v1/invoices")
    app.register_blueprint(blueprint_vendor_orders, url_prefix="/api/v1/vendor_orders")
    # app.register_blueprint(webapp_bp)


app = create_app()
