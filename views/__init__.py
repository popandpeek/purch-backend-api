"""Modules initialization"""

# from . import auth
from . import db
from . import house_items
from . import house_orders
from . import inventories
from . import invoices
from . import vendor_items
from . import vendor_orders
from . import vendors

MODULES = (
    # auth,
    house_items,
    house_orders,
    inventories,
    invoices,
    vendor_items,
    vendor_orders,
    vendors
)


def register_blueprints(api):
    """Initialize application with all modules"""
    for module in MODULES:
        api.register_blueprint(module.blp)
