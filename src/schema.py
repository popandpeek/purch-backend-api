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
    vendor_items = ma.Nested('VendorItemSchema', many=True)
    vendor_orders = ma.Nested('VendorOrderSchema', many=True)
    vendor_invoices = ma.Nested('VendorInvoiceSchema', many=True)


class ItemClassSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    type = ma.String(required=True)
    house_items = ma.Nested('HouseItemSchema', many=True)


class VendorItemSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    active = ma.Boolean(required=True)
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
    vendor_order_items = ma.Nested('VendorOrderItemSchema', many=True)
    vendor = ma.Nested(VendorSchema)


class StorageLocationSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    name = ma.String(required=True)
    storage_type = ma.String(required=True)
    house_items = ma.Nested('HouseItemSchema', many=True)


class HouseItemSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    name = ma.String(required=True)
    description = ma.String(required=True)
    active = ma.Boolean(required=True)
    measure_unit = ma.String(required=True)
    vendor_items = ma.Nested(VendorItemSchema, many=True)
    default_vendor_item_id = ma.Integer(required=False)
    storage_locations = ma.Nested(StorageLocationSchema, many=True)


class StorageLocationHouseItemSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    name = ma.String(required=True)
    description = ma.String(required=True)
    active = ma.Boolean(required=True)
    measure_unit = ma.String(required=True)
    vendor_items = ma.Nested(VendorItemSchema, many=True)
    default_vendor_item_id = ma.Integer(required=False)


class HouseOrderSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    date = ma.DateTime(required=True)
    house_order_items = ma.Nested('HouseOrderItemSchema', many=True)
    submitted = ma.Boolean(required=True)


class HouseOrderItemSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    house_item_id = ma.Integer(required=True)
    house_order_id = ma.Integer(required=True)
    quantity = ma.Decimal(required=True)
    price = ma.Decimal(reqired=True)
    house_item = ma.Nested(HouseItemSchema)
    house_order = ma.Nested(HouseOrderSchema)


class VendorOrderSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    vendor_id = ma.Integer(required=True)
    vendor_invoice_id = ma.Integer(required=True)
    date = ma.DateTime(required=True)
    submitted = ma.Boolean(required=True)
    vendor_order_items = ma.Nested('VendorOrderItemSchema', many=True)
    vendor = ma.Nested(VendorSchema)
    vendor_invoice = ma.Nested('VendorInvoiceSchema')


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
    house_inventory_items = ma.Nested('HouseInventoryItemSchema', many=True)


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
house_inventory_schema = HouseInventorySchema()
house_inventorys_schema = HouseInventorySchema(many=True)
house_inventory_item_schema = HouseInventoryItemSchema()
house_inventory_items_schema = HouseInventoryItemSchema(many=True)