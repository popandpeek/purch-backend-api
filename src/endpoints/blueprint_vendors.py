from flask import jsonify, Blueprint
from src.model import *
from src.schema import *


blueprint_vendors = Blueprint('vendors_bp', __name__)


@blueprint_vendors.route('/get_vendors', methods=['GET'])
# @jwt_required()
def vendors():
    vendor_objs = Vendor.query.all()
    if vendor_objs:
        result = vendors_schema.dump(vendor_objs)
        return jsonify(result), 200
    else:
        return jsonify('No vendors!'), 404


# TODO: add_vendor(): creates new vendor object