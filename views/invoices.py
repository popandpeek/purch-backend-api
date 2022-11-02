from flask.views import MethodView
from extensions.api import Blueprint, SQLCursorPage
from models.model import VendorInvoice
from models.schema import VendorInvoiceSchema
from extensions.database import db


blp = Blueprint('house_invoices', __name__, url_prefix='/invoices', description='Operations on Vendor Invoices')


@blp.route('/<int:vendor_id>/<int:invoice_id>')
class VendorInvoice(MethodView):
    @blp.response(200, VendorInvoiceSchema)
    def get(self, vendor_id, invoice_id):
        """
        Get VendorInvoice
        """
        return VendorInvoice.get_or_404(invoice_id)

    @blp.etag
    @blp.arguments(VendorInvoiceSchema)
    @blp.response(201, VendorInvoiceSchema)
    def put(self, update_data, invoice_id):
        """
        Update VendorInvoice
        """
        invoice = VendorInvoice.get_or_404(invoice_id)
        blp.check_etag(invoice, VendorInvoiceSchema)
        VendorInvoiceSchema().update(invoice, update_data)
        db.session.add(invoice)
        db.session.commit()
        return invoice


@blp.route('/<int:vendor_id>')
# @jwt_required()
class VendorInvoices(MethodView):
    @blp.response(200, VendorInvoiceSchema(many=True))
    def get(self, vendor_id):
        """
        Get list of VendorInvoice's by vendor id
        """
        invoices = VendorInvoice.query.filter(VendorInvoice.vendor_id == vendor_id).order_by(VendorInvoice.date).all()
        return invoices

    @blp.arguments(VendorInvoiceSchema)
    @blp.response(201, VendorInvoiceSchema)
    def post(self, vendor_id, new_invoice):
        """
        Post new VendorInvoice for vendor id
        """
        invoice = VendorInvoice(**new_invoice)
        db.session.add(invoice)
        db.session.commit()
        return invoice
