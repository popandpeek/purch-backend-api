from flask import jsonify, Blueprint, json
from src.model import *
from src.schema import *


blueprint_vendors = Blueprint('vendors_bp', __name__)


@blueprint_vendors.route('/vendors', methods=['GET'])
# @jwt_required()
def vendors():
    vendor_objs = db.session.query(Vendor).all()
    if vendor_objs:
        result = vendors_schema.dumps(vendor_objs)
        return jsonify(json.loads(result)), 200
    else:
        return jsonify('No vendors!'), 404


# TODO: add_vendor(): creates new vendor object