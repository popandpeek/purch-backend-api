from extensions.api import Blueprint, SQLCursorPage
from flask.views import MethodView
from models.model import VendorOrder
from models.schema import VendorOrderSchema
from extensions.database import db


blp = Blueprint('vendor_orders', __name__, url_prefix='/vendor_orders', description='Operations on Vendor Orders')


@blp.route('/<int:vendor_id>')
class VendorOrders(MethodView):
    @blp.response(200, VendorOrderSchema)
    def get(self, vendor_id):
        """
        Get VendorOrder by vendor id
        """
        orders = VendorOrder.query.filter(VendorOrder.vendor_id == vendor_id).order_by(VendorOrder.date).all()
        return orders

    @blp.arguments(VendorOrderSchema)
    @blp.response(201, VendorOrderSchema)
    def post(self, new_data):
        """
        Post VendorOrder for vendor id
        """
        item = VendorOrder.create(**new_data)
        db.session.add(item)
        db.session.commit()
        return item

    @blp.etag
    @blp.arguments(VendorOrderSchema)
    @blp.response(200, VendorOrderSchema)
    def put(self, update_data):
        """
        Update VendorOrder
        """
        vendor_order_id = update_data.pop('vendor_order_id', None)
        if vendor_order_id:
            order = VendorOrder.query.get_or_404(vendor_order_id)
            blp.check_etag(order, VendorOrderSchema)
            VendorOrderSchema().update(order, update_data)
            db.session.add(order)
            db.session.commit()
            return order
