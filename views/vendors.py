from extensions.api import Blueprint, SQLCursorPage
from flask.views import MethodView
from models.model import Vendor
from models.schema import VendorSchema
from extensions.database import db

blp = Blueprint('vendors', __name__, url_prefix='/vendors', description='Operations on Vendors')


@blp.route('/')
class Vendors(MethodView):
    @blp.response(200, VendorSchema(many=True))
    def get(self):
        """
        Get list if Vendors
        """
        vendors = Vendor.query.all()
        return vendors

    @blp.arguments(VendorSchema)
    @blp.response(201, VendorSchema)
    def post(self, new_data):
        """
        Post new Vendor
        """
        vendor = Vendor(**new_data)
        db.session.add(vendor)
        db.session.commit()
        return vendor


@blp.route('/<int:vendor_id>')
class Vendor(MethodView):
    @blp.response(200, VendorSchema)
    def get(self, vendor_id):
        """
        Get Vendor by id
        """
        return Vendor.get_or_404(vendor_id)

    @blp.etag
    @blp.arguments(VendorSchema)
    @blp.response(200, VendorSchema)
    def put(self, update_data, vendor_id):
        """
        Update Vendor
        """
        vendor = Vendor.get_or_404(vendor_id)
        blp.check_etag(vendor, VendorSchema)
        VendorSchema().update(vendor, update_data)
        db.session.add(vendor)
        db.session.commit()
        return vendor

