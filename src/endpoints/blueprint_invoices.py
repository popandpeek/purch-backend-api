from flask import request, jsonify, Blueprint
from src.model import *

blueprint_invoices = Blueprint('house_invoices', __name__)


@blueprint_invoices.route('/get_invoices/<int:vendor_id>', methods=['GET'])
# @jwt_required()
def vendor_invoices(vendor_id: int):
    invoices = VendorInvoice.query.filter_by(VendorInvoice.vendor_id == vendor_id).order_by(VendorInvoice.date)
    if invoices:
        result = vendor_invoice_schema.dump(invoices)
        return jsonify(result), 200
    else:
        return jsonify('No invoices found for this vendor!'), 404


# TODO: add_vendor_invoice(): takes in vendor_id and invoice file, creates vendor_invoice object
@blueprint_invoices.route('/add_invoice', methods=['POST'])
# @jwt_required()
def add_vendor_invoice():
    vendor_id = request.form['vendor_id']
    vendor_order_id = request.form['vendor_order_id']
    date = request.form['date']
    invoice = VendorInvoice(vendor_id=vendor_id, vendor_order_id=vendor_order_id, date=date)
    db.session.add(invoice)
    db.session.commit()
    return jsonify('Vendor invoice successfully added to database.'), 201
