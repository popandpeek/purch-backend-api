from extensions import db, ma
from flask_marshmallow import Marshmallow

house_storage_association_table = db.Table('hs_st_assoc', db.Model.metadata,
                                           db.Column('house_item_id', db.ForeignKey('house_item.id'),
                                                     primary_key=True),
                                           db.Column('storage_location_id',
                                                     db.ForeignKey('storage_location.id'),
                                                     primary_key=True))


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    address_street1 = db.Column(db.String, nullable=False)
    address_street2 = db.Column(db.String)
    address_city = db.Column(db.String, nullable=False)
    address_state = db.Column(db.String, nullable=False)
    address_zip = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean)


class Vendor(db.Model):
    __tablename__ = 'vendor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    account_number = db.Column(db.String, nullable=False)
    address_street1 = db.Column(db.String, nullable=False)
    address_street2 = db.Column(db.String)
    address_city = db.Column(db.String, nullable=False)
    address_state = db.Column(db.String, nullable=False)
    address_zip = db.Column(db.Integer, nullable=False)
    contact_first_name = db.Column(db.String, nullable=False)
    contact_last_name = db.Column(db.String, nullable=False)
    contact_email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False)
    delivery_days = db.Column(db.JSON)
    vendor_items = db.relationship('VendorItem', back_populates='vendor', cascade='all, delete')
    vendor_orders = db.relationship('VendorOrder', back_populates='vendor', cascade='all, delete')
    vendor_invoices = db.relationship('VendorInvoice', back_populates='vendor', cascade='all, delete')


class ItemClassification(db.Model):
    __tablename__ = 'item_classification'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    house_items = db.relationship('HouseItem', back_populates='item_class', cascade='all, delete')


class VendorItem(db.Model):
    __tablename__ = 'vendor_item'
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    house_item_id = db.Column(db.Integer, db.ForeignKey('house_item.id'))
    SKU = db.Column(db.String, nullable=False)
    vendor_product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    measure_unit = db.Column(db.String, nullable=False)
    pack_size = db.Column(db.Integer, nullable=False)
    pack_number = db.Column(db.Integer, nullable=False)
    brand_name = db.Column(db.String, nullable=False)
    vendor_order_items = db.relationship('VendorOrderItem', back_populates='vendor_item', cascade='all, delete')
    vendor = db.relationship('Vendor', back_populates='vendor_items', cascade='all, delete', foreign_keys=[vendor_id])
    house_item = db.relationship('HouseItem', back_populates='vendor_items', cascade='all, delete',
                                 foreign_keys=[house_item_id])


class HouseItem(db.Model):
    __tablename__ = 'house_item'
    id = db.Column(db.Integer, primary_key=True)
    item_class_id = db.Column(db.Integer, db.ForeignKey('item_classification.id'))
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    active = db.Column(db.Boolean)
    inventory_category = db.Column(db.String, nullable=False)
    measure_unit = db.Column(db.String, nullable=False)
    item_class = db.relationship('ItemClassification', back_populates='house_items', cascade='all, delete',
                                 foreign_keys=[item_class_id])
    house_order_items = db.relationship('HouseOrderItem', back_populates='house_item', cascade='all, delete')
    house_inventory_items = db.relationship('HouseInventoryItem', back_populates='house_item', cascade='all, delete')
    vendor_items = db.relationship('VendorItem', back_populates='house_item', cascade='all, delete')
    default_vendor_item_id = db.Column(db.Integer, nullable=True)
    storage_locations = db.relationship('StorageLocation', secondary=house_storage_association_table,
                                        back_populates='house_items', cascade='all, delete')


# house_items added via back_populates in HouseItem.storage_locations relationship
class StorageLocation(db.Model):
    __tablename__ = 'storage_location'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    storage_type = db.Column(db.String)
    house_items = db.relationship('HouseItem', secondary=house_storage_association_table,
                                  back_populates='storage_locations', cascade='all, delete')


class HouseOrder(db.Model):
    __tablename__ = 'house_order'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    submitted = db.Column(db.Boolean)
    house_order_items = db.relationship('HouseOrderItem', back_populates='house_order', cascade='all, delete')


class HouseOrderItem(db.Model):
    __tablename__ = 'house_order_item'
    id = db.Column(db.Integer, primary_key=True)
    house_item_id = db.Column(db.Integer, db.ForeignKey('house_item.id'))
    house_order_id = db.Column(db.Integer, db.ForeignKey('house_order.id'))
    quantity = db.Column(db.Numeric, nullable=False)
    house_order = db.relationship('HouseOrder', back_populates='house_order_items', cascade='all, delete',
                                  foreign_keys=[house_order_id])
    house_item = db.relationship('HouseItem', back_populates='house_order_items', cascade='all, delete',
                                 foreign_keys=[house_item_id])


class VendorOrder(db.Model):
    __tablename__ = 'vendor_order'
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    date = db.Column(db.DateTime, nullable=False)
    submitted = db.Column(db.Boolean)
    vendor = db.relationship('Vendor', back_populates='vendor_orders', foreign_keys=[vendor_id],
                             cascade='all, delete')
    vendor_invoice = db.relationship('VendorInvoice', back_populates='vendor_order', cascade='all, delete')
    vendor_order_items = db.relationship('VendorOrderItem', back_populates='vendor_order', cascade='all, delete')


class VendorOrderItem(db.Model):
    __tablename__ = 'vendor_order_item'
    id = db.Column(db.Integer, primary_key=True)
    vendor_item_id = db.Column(db.Integer, db.ForeignKey('vendor_item.id'))
    vendor_order_id = db.Column(db.Integer, db.ForeignKey('vendor_order.id'))
    price = db.Column(db.Numeric, nullable=False)
    quantity = db.Column(db.Numeric, nullable=False)
    vendor_item = db.relationship('VendorItem', back_populates='vendor_order_items', foreign_keys=[vendor_item_id],
                                  cascade='all, delete')
    vendor_order = db.relationship('VendorOrder', back_populates='vendor_order_items', foreign_keys=[vendor_order_id],
                                   cascade='all, delete')


class VendorInvoice(db.Model):
    __tablename__ = 'vendor_invoice'
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    vendor_order_id = db.Column(db.Integer, db.ForeignKey('vendor_order.id'))
    date = db.Column(db.DateTime, nullable=False)
    vendor_order = db.relationship('VendorOrder', back_populates='vendor_invoice', uselist=False,
                                   foreign_keys=[vendor_order_id], cascade='all, delete')
    vendor = db.relationship('Vendor', back_populates='vendor_invoices', cascade='all, delete', foreign_keys=[vendor_id])
    # invoice_image = db.Column(db.RAW)


class HouseInventory(db.Model):
    __tablename__ = 'house_inventory'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    submitted = db.Column(db.Boolean)
    house_inventory_items = db.relationship('HouseInventoryItem', back_populates='house_inventory', cascade='all, delete')


class HouseInventoryItem(db.Model):
    __tablename__ = 'house_inventory_item'
    id = db.Column(db.Integer, primary_key=True)
    house_item_id = db.Column(db.Integer, db.ForeignKey('house_item.id'))
    house_inventory_id = db.Column(db.Integer, db.ForeignKey('house_inventory.id'))
    date = db.Column(db.DateTime, nullable=False)
    quantity = db.Column(db.Numeric, nullable=False)
    measure_unit = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    house_item = db.relationship('HouseItem', back_populates='house_inventory_items', cascade='all, delete',
                                 foreign_keys=[house_item_id])
    house_inventory = db.relationship('HouseInventory', back_populates='house_inventory_items', cascade='all, delete',
                                      foreign_keys=[house_inventory_id])


class UserSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    address_street1 = ma.String(required=True)
    address_street2 = ma.String()
    address_city = ma.String(required=True)
    address_state = ma.String(required=True)
    address_zip = ma.Integer(required=True)
    phone = ma.String(required=True)
    email = ma.Email(required=True)
    password = ma.String(required=True)
    admin = ma.Boolean(required=True)


class VendorSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    name = ma.String(required=True)
    account_number = ma.String(required=True)
    address_street1 = ma.String(required=True)
    address_street2 = ma.String()
    address_city = ma.String(required=True)
    address_state = ma.String(required=True)
    address_zip = ma.String(required=True)
    contact_first_name = ma.String(required=True)
    contact_last_name = ma.String(required=True)
    contact_email = ma.Email(required=True)
    phone = ma.String(required=True)
    delivery_days = ma.List(ma.String, required=True)
    # vendor_items = ma.Nested(VendorItemSchema, many=True)
    # vendor_orders = ma.Nested(VendorOrderSchema, many=True)
    # vendor_invoices = ma.Nested(VendorInvoiceSchema, many=True)


class ItemClassSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    type = ma.String(required=True)
    # house_items = ma.Nested(HouseItemSchema, many=True)


class VendorItemSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    vendor_id = ma.Integer(required=True)
    house_item_id = ma.Integer(required=True)
    SKU = ma.String(required=True)
    vendor_product_id = ma.Integer(required=True)
    product_name = ma.String(required=True)
    description = ma.String(required=True)
    measure_unit = ma.String(required=True)
    pack_size = ma.Integer(required=True)
    pack_number = ma.Integer(required=True)
    brand_name = ma.String(required=True)
    # vendor_order_items = ma.Nested(VendorOrderItemSchema, many=True)
    vendor = ma.Nested(VendorSchema)


class HouseItemSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    name = ma.String(required=True)
    description = ma.String(required=True)
    active = ma.Boolean(required=True)
    inventory_category = ma.String(required=True)
    measure_unit = ma.String(required=True)
    # house_order_items = ma.Nested(HouseOrderItemSchema, many=True)
    # house_inventory_items = ma.Nested(HouseInventoryItemSchema, many=True)
    vendor_items = ma.Nested(VendorItemSchema, many=True)
    default_vendor_item_id = ma.Integer(required=False)
    # storage_locations = ma.Nested(StorageLocationSchema, many=True)


class StorageLocationSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    name = ma.String(required=True)
    storage_type = ma.String(required=True)
    house_items = ma.Nested(HouseItemSchema, many=True)


class HouseOrderSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    date = ma.DateTime(required=True)
    # house_order_items = ma.Nested(HouseOrderItemSchema, many=True)
    submitted = ma.Boolean(required=True)


class HouseOrderItemSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    house_item_id = ma.Integer(required=True)
    house_order_id = ma.Integer(required=True)
    quantity = ma.Decimal(required=True)
    house_order = ma.Nested(HouseOrderSchema)


class VendorOrderSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    vendor_id = ma.Integer(required=True)
    vendor_invoice_id = ma.Integer(required=True)
    date = ma.DateTime(required=True)
    submitted = ma.Boolean(required=True)
    # vendor_order_items = ma.Nested(VendorOrderItemSchema, many=True)
    vendor = ma.Nested(VendorSchema)
    # vendor_invoice = ma.Nested(VendorInvoiceSchema)


class VendorOrderItemSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    vendor_item_id = ma.Integer(required=True)
    vendor_order_id = ma.Integer(required=True)
    price = ma.Decimal(required=True)
    quantity = ma.Decimal(required=True)
    vendor = ma.Nested(VendorSchema)
    vendor_order = ma.Nested(VendorOrderSchema)


class VendorInvoiceSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    vendor_id = ma.Integer(required=True)
    vendor_order_id = ma.Integer(required=True)
    date = ma.DateTime(required=True)
    invoice_image = ma.Raw(required=True)
    vendor = ma.Nested(VendorSchema)
    vendor_order = ma.Nested(VendorOrderSchema)


class HouseInventorySchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    date = ma.DateTime(required=True)
    submitted = ma.Boolean(required=True)
    # house_inventory_items = ma.Nested(HouseInventoryItemSchema, many=True)


class HouseInventoryItemSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    house_item_id = ma.Integer(required=True)
    house_inventory_id = ma.Integer(requireed=True)
    date = ma.DateTime(required=True)
    quantity = ma.Decimal(required=True)
    measure_unit = ma.String(required=True)
    price = ma.Decimal(required=True)
    house_inventory = ma.Nested(HouseInventorySchema)


user_schema = UserSchema()
vendor_schema = VendorSchema()
vendors_schema = VendorSchema(many=True)
house_item_schema = HouseItemSchema()
house_items_schema = HouseItemSchema(many=True)
vendor_item_schema = VendorItemSchema()
vendor_items_schema = VendorItemSchema(many=True)
item_class_schema = ItemClassSchema()
storage_location_schema = StorageLocationSchema()
storage_locations_schema = StorageLocationSchema(many=True)
house_order_schema = HouseOrderSchema()
house_orders_schema = HouseOrderSchema(many=True)
house_order_item_schema = HouseOrderItemSchema()
house_order_items_schema = HouseOrderItemSchema(many=True)
vendor_order_schema = VendorOrderSchema()
vendor_orders_schema = VendorOrderSchema(many=True)
vendor_order_item_schema = VendorOrderItemSchema()
vendor_order_items_schema = VendorOrderItemSchema(many=True)
vendor_invoice_schema = VendorInvoiceSchema()
vendor_invoices_schema = VendorInvoiceSchema(many=True)
house_inventory_schema = HouseInventorySchema()
house_inventorys_schema = HouseInventorySchema(many=True)
house_inventory_item_schema = HouseInventoryItemSchema()
house_inventory_items_schema = HouseInventoryItemSchema(many=True)
