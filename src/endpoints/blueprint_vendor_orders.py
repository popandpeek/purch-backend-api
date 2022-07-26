from flask import jsonify, Blueprint
from src.model import *
from src.schema import *


blueprint_vendor_orders = Blueprint('house_vendor_bp', __name__)


@blueprint_vendor_orders.route('/orders/<int:vendor_id>', methods=['GET'])
# @jwt_required()
def vendor_orders(vendor_id: int):
    orders = VendorOrder.query.filter_by(VendorOrder.vendor_id == vendor_id).order_by(VendorOrder.date).all()
    if orders:
        result = vendor_order_schema.dump(orders)
        return jsonify(result), 200
    else:
        return jsonify('No orders found for this vendor.'), 404