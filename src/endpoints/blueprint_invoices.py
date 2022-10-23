from flask import request, jsonify, Blueprint, json
from src.model import *
from src.schema import *


blueprint_invoices = Blueprint('house_invoices', __name__)


@blueprint_invoices.route('/invoices/<int:vendor_id>', methods=['GET'])
# @jwt_required()
def vendor_invoices(vendor_id: int):
    invoices = VendorInvoice.query.filter(VendorInvoice.vendor_id == vendor_id).order_by(VendorInvoice.date).all()
    if invoices:
        result = vendor_invoices_schema.dumps(invoices)
        return jsonify(json.loads(result)), 200
    else:
        return jsonify('No invoices found for this vendor!'), 404


# TODO: add_vendor_invoice(): takes in vendor_id and invoice file, creates vendor_invoice object
@blueprint_invoices.route('/invoices', methods=['POST'])
# @jwt_required()
def add_vendor_invoice():
    vendor_id = request.form['vendor_id']
    vendor_order_id = request.form['vendor_order_id']
    date = request.form['date']
    invoice = VendorInvoice(vendor_id=vendor_id, vendor_order_id=vendor_order_id, date=date)
    db.session.add(invoice)
    db.session.commit()
    return jsonify('Vendor invoice successfully added to database.'), 201
