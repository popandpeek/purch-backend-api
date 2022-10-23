from flask import Flask
from config import config
from src.extensions import swag
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec
from flask_swagger_ui import get_swaggerui_blueprint
from src.schema import UserSchema, VendorSchema, VendorInvoiceSchema, VendorItemSchema, VendorOrderSchema, \
    VendorOrderItemSchema, HouseItemSchema, HouseOrderSchema, HouseInventorySchema, HouseInventoryItemSchema, \
    HouseOrderItemSchema, StorageLocationHouseItemSchema, StorageLocationSchema, ItemClassSchema


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    # configure_swagger(app)
    return app


def register_extensions(app):
    from src.extensions import db
    # from src.extensions import jwt_manager
    # from src.extensions import login_manager
    from src.extensions import migrate
    from src.extensions import ma
    ma.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    swag.init_app(app)
    # jwt_manager.init_app(app)
    # login_manager.init_app(app)
    # login_manager.login_view = 'webapp.login'


def register_blueprints(app):
    # from src.extensions import swagger_ui_blueprint, SWAGGER_URL
    from src.endpoints.blueprint_db import blueprint_db
    from src.endpoints.blueprint_users import blueprint_users
    from src.endpoints.blueprint_vendors import blueprint_vendors
    from src.endpoints.blueprint_vendor_items import blueprint_vendor_items
    from src.endpoints.blueprint_house_items import blueprint_house_items
    from src.endpoints.blueprint_house_orders import blueprint_house_orders
    from src.endpoints.blueprint_inventories import blueprint_inventories
    from src.endpoints.blueprint_invoices import blueprint_invoices
    from src.endpoints.blueprint_vendor_orders import blueprint_vendor_orders

    app.register_blueprint(blueprint_db, url_prefix="/api/db")
    # app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(blueprint_users, url_prefix="/api/v1/users")
    app.register_blueprint(blueprint_vendors, url_prefix="/api/v1/vendors")
    app.register_blueprint(blueprint_vendor_items, url_prefix="/api/v1/vendor_items")
    app.register_blueprint(blueprint_house_items, url_prefix="/api/v1/house_items")
    app.register_blueprint(blueprint_house_orders, url_prefix="/api/v1/house_orders")
    app.register_blueprint(blueprint_inventories, url_prefix="/api/v1/inventories")
    app.register_blueprint(blueprint_invoices, url_prefix="/api/v1/invoices")
    app.register_blueprint(blueprint_vendor_orders, url_prefix="/api/v1/vendor_orders")


# def configure_swagger(app: Flask):
#     spec = APISpec(
#         "purch.io", "1.0.0",
#         openapi_version="3.0.2",
#         plugins=[FlaskPlugin(), MarshmallowPlugin()]
#     )
#     template = spec.to_flasgger(
#         app,
#         definitions=[UserSchema, VendorSchema, VendorInvoiceSchema, VendorItemSchema, VendorOrderSchema,
#                      VendorOrderItemSchema, HouseItemSchema, HouseOrderSchema, HouseInventorySchema,
#                      HouseInventoryItemSchema, HouseOrderItemSchema, StorageLocationHouseItemSchema,
#                      StorageLocationSchema, ItemClassSchema]
#     )
#     configs = {
#         "headers": [
#         ],
#         "definitions": template['definitions'],
#         "specs": [
#             {
#                 "endpoint": 'v0_spec',
#                 "route": '/v0',
#                 "version": "0.0.0",
#                 "title": "API v0",
#                 "description": 'Version 0 of the API',
#                 "rule_filter": lambda rule: rule.endpoint.startswith('api_v0'),
#                 "model_filter": lambda tag: True,  # all in
#             },
#             {
#                 "endpoint": 'v1_spec',
#                 "route": '/v1',
#                 "version": "1.0.0",
#                 "title": "API v1",
#                 "description": 'Version 1 of the API',
#                 "rule_filter": lambda rule: rule.endpoint.startswith('api_v1'),
#                 "model_filter": lambda tag: True,  # all in
#             },
#         ],
#         "static_url_path": "/flasgger_static",
#         # "static_folder": "static",  # must be set by user
#         "swagger_ui": True,
#         "specs_route": "/apidocs/",
#         "title": "API",
#         "schemes": [
#             "http",
#             "https"
#         ],
#         "securityDefinitions": {
#             "basicAuth": {
#                 "type": "http",
#                 "scheme": "basic"
#             }
#         },
#         "security": {"basicAuth": []}
#     }


app = create_app()
