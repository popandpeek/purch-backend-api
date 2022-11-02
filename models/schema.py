from extensions.database import *
from models.model import *
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from marshmallow import EXCLUDE


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class VendorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    vendor_items = fields.Nested('VendorItemSchema', many=True, exclude=('vendor', 'vendor_order_items',
                                                                         'vendor_invoice_items',))
    vendor_orders = fields.Nested('VendorOrderSchema', many=True, exclude=('vendor', 'vendor_invoice',
                                                                           'vendor_order_items',))
    vendor_invoices = fields.Nested('VendorInvoiceSchema', many=True, exclude=('vendor', 'vendor_order',
                                                                               'vendor_invoice_items',))

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class ItemClassSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ItemClassification
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    house_items = fields.Nested('HouseItemSchema', many=True, exclude=('house_order_items', 'house_inventory_items',
                                                                       'vendor_items', 'item_class', 'storage_locations'))

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class VendorItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VendorItem
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    vendor_order_items = fields.Nested('VendorOrderItemSchema', many=True, exclude=('vendor_item', 'house_order_item',
                                                                                    'vendor_invoice_item',
                                                                                    'house_order_item'))
    vendor = fields.Nested(VendorSchema, exclude=('vendor_items', 'vendor_orders', 'vendor_invoices',))
    house_item = fields.Nested('HouseItemSchema', exclude=('house_order_items', 'house_inventory_items', 'vendor_items',
                                                           'storage_locations', 'item_class',))
    vendor_invoice_items = fields.Nested('VendorInvoiceItemSchema', many=True, exclude=('vendor_invoice',
                                                                                        'vendor_order_item',
                                                                                        'vendor_item'))

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class StorageLocationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StorageLocation
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    house_items = fields.Nested('HouseItemSchema', many=True, exclude=('house_order_items', 'house_inventory_items',
                                                                       'vendor_items', 'storage_locations', 'item_class', ))

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class StorageLocationHouseItemSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    name = ma.String(required=True)
    description = ma.String(required=True)
    active = ma.Boolean(required=True)
    measure_unit = ma.String(required=True)
    default_vendor_item_id = ma.Integer(required=False)
    vendor_items = fields.Nested(VendorItemSchema, many=True, exclude=('vendor_order_items', 'vendor',
                                                                       'house_item', 'vendor_invoice_items'))

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class HouseItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = HouseItem
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    item_class = fields.Nested(ItemClassSchema, exclude=('house_items',))
    house_order_items = fields.Nested('HouseOrderItemSchema', many=True, exclude=('vendor_order_item', 'house_item',
                                                                                  'house_order',))
    house_inventory_items = fields.Nested('HouseInventoryItemSchema', exclude=('house_item', 'house_inventory'))
    vendor_items = fields.Nested(VendorItemSchema, many=True, exclude=('vendor_order_items', 'vendor', 'house_item',
                                                                       'vendor_invoice_items',))
    storage_locations = fields.Nested(StorageLocationSchema, many=True, exclude=('house_items',))

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class HouseOrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = HouseOrder
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    house_order_items = fields.Nested('HouseOrderItemSchema', many=True, exclude=('house_order', 'house_item',
                                                                                  'vendor_order_item', ))

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class HouseOrderItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = HouseOrderItem
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    house_order = fields.Nested(HouseOrderSchema, exclude=('house_order_items',))
    house_item = fields.Nested(HouseItemSchema, exclude=('house_order_items', 'house_inventory_items', 'vendor_items',
                                                         'storage_locations'))
    vendor_order_item = fields.Nested('VendorOrderItemSchema', exclude=('vendor_order', 'vendor_item', 'house_order_item',
                                                                        'vendor_invoice_item',))

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class VendorOrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VendorOrder
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    vendor = fields.Nested(VendorSchema, exclude=('vendor_items', 'vendor_orders', 'vendor_invoices',))
    vendor_invoice = fields.Nested('VendorInvoiceSchema', exclude=('vendor', 'vendor_order', 'vendor_invoice_items',))
    vendor_order_items = fields.Nested('VendorOrderItemSchema', many=True, exclude=('vendor_item', 'vendor_order',
                                                                                    'vendor_invoice_item',
                                                                                    'house_order_item'))

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class VendorOrderItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VendorOrderItem
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    vendor_item = fields.Nested(VendorItemSchema, exclude=('vendor_order_items', 'vendor', 'house_item',
                                                           'vendor_invoice_items'))
    vendor_order = fields.Nested(VendorOrderSchema, exclude=('vendor', 'vendor_invoice', 'vendor_order_items',))
    vendor_invoice_item = fields.Nested('VendorInvoiceItemSchema', exclude=('vendor_invoice', 'vendor_order_item',
                                                                            'vendor_item',))
    house_order_item = fields.Nested(HouseOrderItemSchema, exclude=('house_order', 'house_item', 'vendor_order_item'))

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class VendorInvoiceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VendorInvoice
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    vendor = fields.Nested(VendorSchema, exclude=('vendor_orders', 'vendor_invoices', 'vendor_items',))
    vendor_order = fields.Nested(VendorOrderSchema, exclude=('vendor', 'vendor_invoice', 'vendor_order_items',))
    vendor_invoice_items = fields.Nested('VendorInvoiceItemSchema', many=True, exclude=('vendor_invoice',
                                                                                        'vendor_order_item',
                                                                                        'vendor_item',))

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class VendorInvoiceItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VendorInvoiceItem
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    vendor_invoice = fields.Nested(VendorInvoiceSchema, exclude=('vendor', 'vendor_order', 'vendor_invoice_items',))
    vendor_order_item = fields.Nested(VendorOrderItemSchema, exclude=('vendor_item', 'vendor_order', 'vendor_invoice_item',
                                                                      'house_order_item',))
    vendor_item = fields.Nested(VendorItemSchema, exclude=('vendor_order_items', 'vendor', 'house_item',
                                                           'vendor_invoice_items',))

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class HouseInventorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = HouseInventory
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    house_inventory_items = fields.Nested('HouseInventoryItemSchema', many=True, exclude=('house_item',
                                                                                          'house_inventory', ))

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class HouseInventoryItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = HouseInventoryItem
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    house_item = fields.Nested(HouseItemSchema)
    house_inventory = fields.Nested(HouseInventorySchema, exclude=('house_inventory_items',))

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


# user_schema = UserSchema()
# vendor_schema = VendorSchema()
# vendors_schema = VendorSchema(many=True)
# house_item_schema = HouseItemSchema()
# house_items_schema = HouseItemSchema(many=True)
# vendor_item_schema = VendorItemSchema()
# vendor_items_schema = VendorItemSchema(many=True)
# item_class_schema = ItemClassSchema()
# storage_location_schema = StorageLocationSchema()
# storage_locations_schema = StorageLocationSchema(many=True)
# location_items_schema = StorageLocationHouseItemSchema(many=True)
# house_order_schema = HouseOrderSchema()
# house_orders_schema = HouseOrderSchema(many=True)
# house_order_item_schema = HouseOrderItemSchema()
# house_order_items_schema = HouseOrderItemSchema(many=True)
# vendor_order_schema = VendorOrderSchema()
# vendor_orders_schema = VendorOrderSchema(many=True)
# vendor_order_item_schema = VendorOrderItemSchema()
# vendor_order_items_schema = VendorOrderItemSchema(many=True)
# vendor_invoice_schema = VendorInvoiceSchema()
# vendor_invoices_schema = VendorInvoiceSchema(many=True)
# vendor_invoice_item_schema = VendorInvoiceItemSchema()
# vendor_invoice_items_schema = VendorInvoiceItemSchema(many=True)
# house_inventory_schema = HouseInventorySchema()
# house_inventorys_schema = HouseInventorySchema(many=True)
# house_inventory_item_schema = HouseInventoryItemSchema()
# house_inventory_items_schema = HouseInventoryItemSchema(many=True)
