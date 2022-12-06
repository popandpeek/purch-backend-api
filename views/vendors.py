from flask import request, jsonify, json
from extensions.api import Blueprint
from flask.views import MethodView
from models.model import Vendor
from models.schema import VendorSchema
from extensions.database import db
from werkzeug.datastructures import MultiDict


blp = Blueprint('vendors', __name__, url_prefix='/vendors', description='Operations on Vendors')


@blp.route('/')
class Vendors(MethodView):
    @blp.response(200, VendorSchema(many=True))
    def get(self):
        """
        Get list of Vendors
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


@blp.route('/list/')
class VendorsList(MethodView):
    @blp.response(200, VendorSchema(many=True))
    def get(self):
        """
        Get list of Vendors from list of ids
        """
        print('Got to get request for /list!')
        vendors_list = []
        vendor_ids = MultiDict(request.args)
        print(vendor_ids)
        ids_only = vendor_ids.getlist('vendor_ids[]')
        for i in ids_only:
            i = int(i)
            print(i)
            v = Vendor.query.get_or_404(i)
            vendors_list.append(v)

        return vendors_list


@blp.route('/<int:vendor_id>')
class VendorSingle(MethodView):
    @blp.response(200, VendorSchema)
    def get(self, vendor_id):
        """
        Get Vendor by id
        """
        return Vendor.query.get_or_404(vendor_id)

    @blp.etag
    @blp.arguments(VendorSchema)
    @blp.response(200, VendorSchema)
    def put(self, update_data, vendor_id):
        """
        Update Vendor
        """
        vendor = Vendor.query.get_or_404(vendor_id)
        blp.check_etag(vendor, VendorSchema)
        VendorSchema().update(vendor, update_data)
        db.session.add(vendor)
        db.session.commit()
        return vendor

