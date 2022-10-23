from src.extensions import db

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
    active = db.Column(db.Boolean)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    house_item_id = db.Column(db.Integer, db.ForeignKey('house_item.id'))
    vendor_SKU = db.Column(db.String, nullable=False)
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
    vendor_invoice_items = db.relationship('VendorInvoiceItem', back_populates='vendor_item', cascade='all, delete')


class HouseItem(db.Model):
    __tablename__ = 'house_item'
    id = db.Column(db.Integer, primary_key=True)
    item_class_id = db.Column(db.Integer, db.ForeignKey('item_classification.id'))
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    active = db.Column(db.Boolean)
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
    user_id = db.Column(db.Integer, nullable=True)


class HouseOrderItem(db.Model):
    __tablename__ = 'house_order_item'
    id = db.Column(db.Integer, primary_key=True)
    house_item_id = db.Column(db.Integer, db.ForeignKey('house_item.id'))
    house_order_id = db.Column(db.Integer, db.ForeignKey('house_order.id'))
    quantity = db.Column(db.String, nullable=False)
    measure_unit = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=True)
    house_order = db.relationship('HouseOrder', back_populates='house_order_items', cascade='all, delete',
                                  foreign_keys=[house_order_id])
    house_item = db.relationship('HouseItem', back_populates='house_order_items', cascade='all, delete',
                                 foreign_keys=[house_item_id])
    vendor_order_item = db.relationship('VendorOrderItem', back_populates='house_order_item', uselist=False, cascade='all, delete')

class VendorOrder(db.Model):
    __tablename__ = 'vendor_order'
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    date = db.Column(db.DateTime, nullable=False)
    submitted = db.Column(db.Boolean)
    vendor = db.relationship('Vendor', back_populates='vendor_orders', foreign_keys=[vendor_id],
                             cascade='all, delete')
    vendor_invoice = db.relationship('VendorInvoice', back_populates='vendor_order', cascade='all, delete', uselist=False)
    vendor_order_items = db.relationship('VendorOrderItem', back_populates='vendor_order', cascade='all, delete')


class VendorOrderItem(db.Model):
    __tablename__ = 'vendor_order_item'
    id = db.Column(db.Integer, primary_key=True)
    vendor_item_id = db.Column(db.Integer, db.ForeignKey('vendor_item.id'))
    vendor_order_id = db.Column(db.Integer, db.ForeignKey('vendor_order.id'))
    house_order_item_id = db.Column(db.Integer, db.ForeignKey('house_order_item.id'))
    price = db.Column(db.String, nullable=False)
    quantity = db.Column(db.String, nullable=False)
    measure_unit = db.Column(db.String, nullable=False)
    vendor_item = db.relationship('VendorItem', back_populates='vendor_order_items', foreign_keys=[vendor_item_id],
                                  cascade='all, delete')
    vendor_order = db.relationship('VendorOrder', back_populates='vendor_order_items', foreign_keys=[vendor_order_id],
                                   cascade='all, delete')
    vendor_invoice_item = db.relationship('VendorInvoiceItem', back_populates='vendor_order_item', cascade='all, delete', uselist=False)
    house_order_item = db.relationship('HouseOrderItem', back_populates='vendor_order_item', cascade='all, delete')

class VendorInvoice(db.Model):
    __tablename__ = 'vendor_invoice'
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    vendor_order_id = db.Column(db.Integer, db.ForeignKey('vendor_order.id'))
    date = db.Column(db.DateTime, nullable=False)
    paid = db.Column(db.Boolean, nullable=False)
    invoice_image = db.Column(db.Text, nullable=True)
    vendor = db.relationship('Vendor', back_populates='vendor_invoices', cascade='all, delete', foreign_keys=[vendor_id])
    vendor_order = db.relationship('VendorOrder', back_populates='vendor_invoice', cascade='all, delete')
    vendor_invoice_items = db.relationship('VendorInvoiceItem', back_populates='vendor_invoice', cascade='all, delete')


class VendorInvoiceItem(db.Model):
    __tablename__ = 'vendor_invoice_item'
    id = db.Column(db.Integer, primary_key=True)
    vendor_invoice_id = db.Column(db.Integer, db.ForeignKey('vendor_invoice.id'))
    vendor_order_item_id = db.Column(db.Integer, db.ForeignKey('vendor_order_item.id'))
    vendor_item_id = db.Column(db.Integer, db.ForeignKey('vendor_item.id'))
    measure_unit = db.Column(db.String, nullable=False)
    pack_size = db.Column(db.String, nullable=False)
    pack_number = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    quantity = db.Column(db.String, nullable=False)
    vendor_invoice = db.relationship('VendorInvoice', back_populates='vendor_invoice_items', cascade='all, delete',
                                     foreign_keys=[vendor_invoice_id])
    vendor_order_item = db.relationship('VendorOrderItem', back_populates='vendor_invoice_item', cascade='all, delete',
                                   foreign_keys=[vendor_order_item_id])
    vendor_item = db.relationship('VendorItem', back_populates='vendor_invoice_items', cascade='all, delete',
                                  foreign_keys=[vendor_item_id])
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
    quantity = db.Column(db.String, nullable=False)
    measure_unit = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    house_item = db.relationship('HouseItem', back_populates='house_inventory_items', cascade='all, delete',
                                 foreign_keys=[house_item_id])
    house_inventory = db.relationship('HouseInventory', back_populates='house_inventory_items', cascade='all, delete',
                                      foreign_keys=[house_inventory_id])
