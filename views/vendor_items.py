from flask.views import MethodView
from extensions.api import Blueprint, SQLCursorPage
from models.model import VendorItem
from models.schema import VendorItemSchema
from extensions.database import db


blp = Blueprint('vendor_items', __name__, url_prefix='/vendor_items', description='Operations on Vendor Items')


@blp.route('/')
class VendorItemsAll(MethodView):
    @blp.response(200, VendorItemSchema(many=True))
    def get(self):
        """
        Get list of all VendorItem's by
        """
        items = VendorItem.query.all()
        return items


@blp.route('/<int:vendor_id>')
class VendorItems(MethodView):
    @blp.response(200, VendorItemSchema(many=True))
    def get(self, vendor_id):
        """
        Get list of VendorItem's by vendor id
        """
        vendor_items = VendorItem.query.filter_by(vendor_id)
        return vendor_items

    @blp.arguments(VendorItemSchema)
    @blp.response(201, VendorItemSchema)
    def post(self, new_item, vendor_id):
        """
        Post VendorItem
        """
        vendor_item = VendorItem.create(**new_item)
        db.session.add(vendor_item)
        db.session.commit()
        return vendor_item

    @blp.etag
    @blp.arguments(VendorItemSchema)
    @blp.response(200, VendorItemSchema)
    def put(self, update_data, vendor_id):
        """
        Update VendorItem
        """
        vendor_item_id = update_data.pop('vendor_item_id', None)
        if vendor_item_id:
            vendor_item = VendorItem.query.get_or_404(vendor_item_id)
            blp.check_etag(vendor_item, VendorItemSchema)
            VendorItemSchema().update(vendor_item, update_data)
            db.session.add(vendor_item)
            db.session.commit()
            return vendor_item
