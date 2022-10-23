from src.extensions import ma


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
    vendor_items = ma.Nested('VendorItemSchema', many=True, exclude=('vendor', 'vendor_order_items',
                                                                     'vendor_invoice_items', ))
    vendor_orders = ma.Nested('VendorOrderSchema', many=True, exclude=('vendor', 'vendor_order_items',
                                                                       'vendor_invoice_items',))
    vendor_invoices = ma.Nested('VendorInvoiceSchema', many=True, exclude=('vendor', 'vendor_order',
                                                                           'vendor_invoice_items', ))


class ItemClassSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    type = ma.String(required=True)
    house_items = ma.Nested('HouseItemSchema', many=True, exclude=('house_order_items', 'house_inventory_items',
                                                                   'vendor_items', 'item_class', 'storage_locations'))


class VendorItemSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    active = ma.Boolean(required=True)
    vendor_id = ma.Integer(required=True)
    house_item_id = ma.Integer(required=True)
    vendor_SKU = ma.String(required=True)
    vendor_product_id = ma.Integer(required=True)
    product_name = ma.String(required=True)
    description = ma.String(required=True)
    measure_unit = ma.String(required=True)
    pack_size = ma.Integer(required=True)
    pack_number = ma.Integer(required=True)
    brand_name = ma.String(required=True)
    vendor_order_items = ma.Nested('VendorOrderItemSchema', many=True, exclude=('vendor_item', 'house_order_item',
                                                                                'vendor_invoice_item',
                                                                                'house_order_item'))
    vendor = ma.Nested(VendorSchema, exclude=('vendor_items', 'vendor_orders', 'vendor_invoices', ))
    house_item = ma.Nested('HouseItemSchema', exclude=('house_order_items', 'house_inventory_items', 'vendor_items',
                                                       'storage_locations', 'item_class', ))
    vendor_invoice_items = ma.Nested('VendorInvoiceItemSchema', many=True, exclude=('vendor_invoice',
                                                                                    'vendor_order_item',
                                                                                    'vendor_item'))


class StorageLocationSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    name = ma.String(required=True)
    storage_type = ma.String(required=True)
    house_items = ma.Nested('HouseItemSchema', many=True, exclude=('house_order_items', 'house_inventory_items',
                                                                   'vendor_items', 'storage_locations', 'item_class', ))


class StorageLocationHouseItemSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    name = ma.String(required=True)
    description = ma.String(required=True)
    active = ma.Boolean(required=True)
    measure_unit = ma.String(required=True)
    vendor_items = ma.Nested(VendorItemSchema, many=True, exclude=('vendor_order_items', 'vendor', 'house_item',
                                                                   'vendor_invoice_items'))
    default_vendor_item_id = ma.Integer(required=False)


class HouseItemSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    name = ma.String(required=True)
    description = ma.String(required=True)
    active = ma.Boolean(required=True)
    measure_unit = ma.String(required=True)
    item_class = ma.Nested(ItemClassSchema, exclude=('house_items', ))
    house_order_items = ma.Nested('HouseOrderItemSchema', many=True, exclude=('vendor_order_item', 'house_item',
                                                                              'house_order',))
    house_inventory_items = ma.Nested('HouseInventoryItemSchema', exclude=('house_item', 'house_inventory'))
    vendor_items = ma.Nested(VendorItemSchema, many=True, exclude=('vendor_order_items', 'vendor', 'house_item',
                                                                   'vendor_invoice_items', ))
    default_vendor_item_id = ma.Integer(required=False)
    storage_locations = ma.Nested(StorageLocationSchema, many=True, exclude=('house_items', ))


class HouseOrderSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    date = ma.DateTime(required=True)
    house_order_items = ma.Nested('HouseOrderItemSchema', many=True,
                                  exclude=('house_order', 'house_item', 'vendor_order_item', ))
    submitted = ma.Boolean(required=True)
    user_id = ma.Integer(required=False)


class HouseOrderItemSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    house_item_id = ma.Integer(required=True)
    house_order_id = ma.Integer(required=True)
    vendor_order_item_id = ma.Integer(required=True)
    quantity = ma.String(required=True)
    measure_unit = ma.String(required=True)
    price = ma.String(reqired=False)
    house_order = ma.Nested(HouseOrderSchema, exclude=('house_order_items', ))
    house_item = ma.Nested(HouseItemSchema, exclude=('house_order_items', 'house_inventory_items', 'vendor_items',
                                                     'storage_locations'))
    vendor_order_item = ma.Nested('VendorOrderItemSchema', exclude=('vendor_order', 'vendor_item', 'house_order_item',
                                                                    'vendor_invoice_item', ))


class VendorOrderSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    vendor_id = ma.Integer(required=True)
    vendor_invoice_id = ma.Integer(required=True)
    date = ma.DateTime(required=True)
    submitted = ma.Boolean(required=True)
    vendor = ma.Nested(VendorSchema, exclude=('vendor_items', 'vendor_orders', 'vendor_invoices', ))
    vendor_invoice = ma.Nested('VendorInvoiceSchema', exclude=('vendor', 'vendor_order', 'vendor_invoice_items', ))
    vendor_order_items = ma.Nested('VendorOrderItemSchema', many=True, exclude=('vendor_item', 'vendor_order',
                                                                                'vendor_invoice_item',
                                                                                'house_order_item'))


class VendorOrderItemSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    vendor_item_id = ma.Integer(required=True)
    vendor_order_id = ma.Integer(required=True)
    vendor_invoice_item_id = ma.Integer(required=True)
    house_order_item_id = ma.Integer(required=True)
    price = ma.String(required=True)
    quantity = ma.String(required=True)
    measure_unit = ma.String(required=True)
    vendor_item = ma.Nested(VendorItemSchema, exclude=('vendor_order_items', 'vendor', 'house_item',
                                                       'vendor_invoice_items'))
    vendor_order = ma.Nested(VendorOrderSchema, exclude=('vendor', 'vendor_invoice', 'vendor_order_items', ))
    vendor_invoice_item = ma.Nested('VendorInvoiceItemSchema', exclude=('vendor_invoice', 'vendor_order_item',
                                                                        'vendor_item', ))
    house_order_item = ma.Nested(HouseOrderItemSchema, exclude=('house_order', 'house_item', 'vendor_order_item'))


class VendorInvoiceSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    vendor_id = ma.Integer(required=True)
    vendor_order_id = ma.Integer(required=True)
    vendor_invoice_id = ma.Integer(required=True)
    date = ma.DateTime(required=True)
    paid = ma.Boolean(required=True)
    invoice_image = ma.Raw(required=False)
    vendor = ma.Nested(VendorSchema, exclude=('vendor_orders', 'vendor_invoices', 'vendor_items', ))
    vendor_order = ma.Nested(VendorOrderSchema, exclude=('vendor', 'vendor_invoice', 'vendor_order_items', ))
    vendor_invoice_items = ma.Nested('VendorInvoiceItemSchema', exclude=('vendor_invoice', 'vendor_order_item',
                                                                         'vendor_item', ))


class VendorInvoiceItemSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    vendor_invoice_id = ma.Integer(required=True)
    vendor_order_item_id = ma.Integer(required=True)
    vendor_item_id = ma.Integer(required=True)
    measure_unit = ma.String(required=True)
    pack_size = ma.Integer(required=True)
    pack_number = ma.Integer(required=True)
    price = ma.String(required=True)
    quantity = ma.String(required=True)
    vendor_invoice = ma.Nested(VendorInvoiceSchema, exclude=('vendor', 'vendor_order', 'vendor_invoice_items', ))
    vendor_order_item = ma.Nested(VendorOrderItemSchema, exclude=('vendor_item', 'vendor_order', 'vendor_invoice_item',
                                                                  'house_order_item', ))
    vendor_item = ma.Nested(VendorItemSchema, exclude=('vendor_order_items', 'vendor', 'house_item',
                                                       'vendor_invoice_items', ))


class HouseInventorySchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    date = ma.DateTime(required=True)
    submitted = ma.Boolean(required=True)
    house_inventory_items = ma.Nested('HouseInventoryItemSchema', many=True, exclude=('house_item', 'house_inventory', ))


class HouseInventoryItemSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    house_item_id = ma.Integer(required=True)
    house_inventory_id = ma.Integer(requireed=True)
    date = ma.DateTime(required=True)
    quantity = ma.String(required=True)
    measure_unit = ma.String(required=True)
    price = ma.String(required=True)
    house_item = ma.Nested(HouseItemSchema)
    house_inventory = ma.Nested(HouseInventorySchema, exclude=('house_inventory_items', ))


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
location_items_schema = StorageLocationHouseItemSchema(many=True)
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
vendor_invoice_item_schema = VendorInvoiceItemSchema()
vendor_invoice_items_schema = VendorInvoiceItemSchema(many=True)
house_inventory_schema = HouseInventorySchema()
house_inventorys_schema = HouseInventorySchema(many=True)
house_inventory_item_schema = HouseInventoryItemSchema()
house_inventory_items_schema = HouseInventoryItemSchema(many=True)