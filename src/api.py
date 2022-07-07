from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, create_access_token
from sqlalchemy import DateTime, func
from extensions import jwt_manager
from model import *

api_bp = Blueprint('api_bp', __name__)


@api_bp.cli.command('db_create')
def db_create():
    db.create_all()
    db.session.commit()


@api_bp.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("Database dropped.")


@api_bp.cli.command('db_seed')
def db_seed():
    # STORAGE LOCATIONS
    kitchen_line_refer = StorageLocation(
        name='kitchen_line_refer',
        storage_type='refrigeration'
    )
    kitchen_walkin_refer = StorageLocation(
        name='kitchen_walkin_refer',
        storage_type='refrigeration'
    )
    kitchen_walkin_freeze = StorageLocation(
        name='kitchen_walkin_freeze',
        storage_type='freezer'
    )
    kitchen_dry_storage = StorageLocation(
        name='kitchen_dry_storage',
        storage_type='food-dry'
    )
    kitchen_upstairs = StorageLocation(
        name='kitchen_upstairs',
        storage_type='non-food-dry'
    )
    main_server_storage = StorageLocation(
        name='main_server_storage',
        storage_type='non-food-dry'
    )
    bar_room_storage = StorageLocation(
        name='bar_room_storage',
        storage_type='non-food-dry'
    )
    liquor_storage_room = StorageLocation(
        name='liquor_storage_room',
        storage_type='liquor'
    )
    bar_walkin_refer = StorageLocation(
        name='bar_walkin_refer',
        storage_type='beer, wine, beverages'
    )

    # USERS
    user1 = User(
        first_name='Bob',
        last_name='Rossman',
        address_street1='23720 34th Ave W',
        address_street2='',
        address_city='Brier',
        address_state='WA',
        address_zip='98036',
        phone='2063833668',
        email='bob@rossman.com',
        password='opensesame',
        admin=True
    )

    # VENDOR ORDER ITEMS
    v_order_item1 = VendorOrderItem(
        price='0.55',
        quantity='40',
    )
    v_order_item2 = VendorOrderItem(
        price='0.82',
        quantity='40',
    )
    v_order_item3 = VendorOrderItem(
        price='0.54',
        quantity='80',
    )
    v_order_item4 = VendorOrderItem(
        price='0.73',
        quantity='80',
    )

    # HOUSE_ORDER_ITEMS
    order_item1 = HouseOrderItem(
        quantity='40',
    )
    order_item2 = HouseOrderItem(
        quantity='40',
    )
    order_item3 = HouseOrderItem(
        quantity='80',
    )
    order_item4 = HouseOrderItem(
        quantity='80',
    )

    # HOUSE INVENTORY ITEMS
    house_inventory_item1 = HouseInventoryItem(
        date=DateTime.DateTime(2020, 9, 30),
        quantity='27',
        measure_unit='pound',
        price='0.65',
    )
    house_inventory_item2 = HouseInventoryItem(
        date=DateTime.DateTime(2020, 9, 30),
        quantity='12',
        measure_unit='pound',
        price='0.78',
    )

    # HOUSE ORDERS
    order1 = HouseOrder(
        date=DateTime.DateTime(2020, 9, 18),
        submitted=True,
        house_order_items=[order_item1, order_item2]
    )
    order2 = HouseOrder(
        date=DateTime.DateTime(2020, 9, 28),
        submitted=True,
        house_order_items=[order_item3, order_item4]
    )

    # VENDOR ORDERS
    vendor_order1 = VendorOrder(
        date=DateTime.DateTime(2020, 9, 18),
        submitted=True,
        vendor_order_items=[v_order_item1],
    )
    vendor_order2 = VendorOrder(
        date=DateTime.DateTime(2020, 9, 18),
        submitted=True,
        vendor_order_items=[v_order_item2],
    )
    vendor_order3 = VendorOrder(
        date=DateTime.DateTime(2020, 9, 28),
        submitted=True,
        vendor_order_items=[v_order_item3, v_order_item4],
    )

    # HOUSE INVENTORIES
    house_inventory = HouseInventory(
        date=DateTime.DateTime(2020, 9, 30),
        submitted=True,
        house_inventory_items=[house_inventory_item1, house_inventory_item2]
    )

    # ITEM CLASSES
    liquor = ItemClassification(
        type='liquor'
    )
    beer = ItemClassification(
        type='beer'
    )
    wine = ItemClassification(
        type='wine'
    )
    na_beverage = ItemClassification(
        type='na_beverage'
    )
    supplies_bar = ItemClassification(
        type='supplies_bar'
    )
    supplies_restaurant = ItemClassification(
        type='supplies_restaurant'
    )
    supplies_kitchen = ItemClassification(
        type='supplies_kitchen'
    )
    produce = ItemClassification(
        type='produce'
    )
    seafood = ItemClassification(
        type='seafood'
    )
    meat = ItemClassification(
        type='meat'
    )
    dry_goods = ItemClassification(
        type='dry_goods'
    )
    freezer_goods = ItemClassification(
        type='freezer_goods'
    )

    # VENDOR INVOICES
    vendor_invoice1 = VendorInvoice(
        date=DateTime.DateTime(2020, 9, 18),
        vendor_order=vendor_order1
    )
    vendor_invoice2 = VendorInvoice(
        date=DateTime.DateTime(2020, 9, 18),
        vendor_order=vendor_order2
    )
    vendor_invoice3 = VendorInvoice(
        date=DateTime.DateTime(2020, 9, 28),
        vendor_order=vendor_order3
    )

    # VENDOR ITEMS
    carrots_vendor1 = VendorItem(
        SKU='444465354654',
        active=True,
        vendor_product_id=123,
        product_name='Carrots, raw',
        description='Bulk carrots, 40#',
        measure_unit='pounds',
        pack_size=40,
        pack_number=1,
        brand_name='Thumper',
        vendor_order_items=[v_order_item3]
    )
    potato_vendor = VendorItem(
        SKU='5630785467',
        active=True,
        vendor_product_id=8765,
        product_name='Potatoes, #2',
        description='Best bakers',
        measure_unit='case',
        pack_size=1,
        pack_number=40,
        brand_name='Idaho Spuds',
        vendor_order_items=[v_order_item2, v_order_item4]
    )
    carrots_vendor2 = VendorItem(
        SKU='63645689453',
        active=True,
        vendor_product_id=132,
        product_name='Carrots, raw',
        description='Bulk carrots, 40#',
        measure_unit='pounds',
        pack_size=40,
        pack_number=1,
        brand_name='Sunshine',
        vendor_order_items=[v_order_item1]
    )

    # HOUSE ITEMS
    carrots_house = HouseItem(
        name='carrots, raw, bulk',
        description='Carrots, bulk',
        active=True,
        inventory_category='produce',
        measure_unit='case',
        house_order_items=[order_item1, order_item3],
        house_inventory_items=[house_inventory_item1],
        vendor_items=[carrots_vendor1, carrots_vendor2],
        # default_vendor_item_id='',
        storage_locations=[kitchen_dry_storage],
        item_class=produce
    )
    potato_house = HouseItem(
        name='potato, #2, raw',
        description='#2 Bakers, bulk',
        active=True,
        inventory_category='produce',
        measure_unit='case',
        house_order_items=[order_item2, order_item4],
        house_inventory_items=[house_inventory_item2],
        vendor_items=[potato_vendor],
        # default_vendor_item_id=,
        storage_locations=[kitchen_dry_storage],
        item_class=produce
    )

    # VENDORS
    vendor1 = Vendor(
        name='Charlies Produce',
        account_number='111111111',
        address_street1='999 Delridge Way',
        address_street2='',
        address_city='Renton',
        address_state='WA',
        address_zip='98044',
        contact_first_name='Tim',
        contact_last_name='Payne',
        contact_email='bringpayne@charlies.com',
        phone='206-222-6574',
        delivery_days=['Thursday', 'Friday', 'Saturday'],
        vendor_items=[carrots_vendor1, potato_vendor],
        vendor_orders=[vendor_order1, vendor_order3],
        vendor_invoices=[vendor_invoice1, vendor_invoice3]
    )
    vendor2 = Vendor(
        name='Chef Store',
        account_number='999999999',
        address_street1='2256 Bothell Way',
        address_street2='',
        address_city='Bothell',
        address_state='WA',
        address_zip='98012',
        contact_first_name='Rocky',
        contact_last_name='Dalbert',
        contact_email='info@cashncarry.com',
        phone='425-345-9866',
        delivery_days=['Sunday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        vendor_items=[carrots_vendor2],
        vendor_orders=[vendor_order2],
        vendor_invoices=[vendor_invoice2]
    )

    # USERS
    db.session.add(user1)

    # STORAGE LOCATIONS
    db.session.add(kitchen_line_refer)
    db.session.add(kitchen_walkin_refer)
    db.session.add(kitchen_walkin_freeze)
    db.session.add(kitchen_dry_storage)
    db.session.add(kitchen_upstairs)
    db.session.add(main_server_storage)
    db.session.add(bar_room_storage)
    db.session.add(liquor_storage_room)
    db.session.add(bar_walkin_refer)

    # VENDOR_ORDER_ITEMS
    db.session.add(v_order_item1)
    db.session.add(v_order_item2)
    db.session.add(v_order_item3)
    db.session.add(v_order_item4)

    # HOUSE_ORDER_ITEMS
    db.session.add(order_item1)
    db.session.add(order_item2)
    db.session.add(order_item3)
    db.session.add(order_item4)

    # HOUSE_INVENTORY_ITEMS
    db.session.add(house_inventory_item1)
    db.session.add(house_inventory_item2)

    # VENDOR_ORDERS
    db.session.add(vendor_order1)
    db.session.add(vendor_order2)

    # HOUSE_ORDERS
    db.session.add(order1)
    db.session.add(order2)

    # HOUSE_INVENTORY
    db.session.add(house_inventory)

    # VENDOR_ITEMS
    db.session.add(potato_vendor)
    db.session.add(carrots_vendor1)
    db.session.add(carrots_vendor2)

    # VENDOR_INVOICES
    db.session.add(vendor_invoice1)
    db.session.add(vendor_invoice2)

    # HOUSE_ITEMS
    db.session.add(carrots_house)
    db.session.add(potato_house)

    # ITEM_CLASSIFICATION
    db.session.add(liquor)
    db.session.add(beer)
    db.session.add(wine)
    db.session.add(na_beverage)
    db.session.add(supplies_bar)
    db.session.add(supplies_restaurant)
    db.session.add(supplies_kitchen)
    db.session.add(produce)
    db.session.add(seafood)
    db.session.add(meat)
    db.session.add(dry_goods)
    db.session.add(freezer_goods)

    # VENDORS
    db.session.add(vendor1)
    db.session.add(vendor2)

    db.session.commit()


@api_bp.route('/')
def hello_world():
    return 'Hello World!'


def set_default_vendor_item_helper(house_item_id):
    item_id = 0
    lowest_price = float('inf')
    house_item = HouseItem.query.filter_by(id=house_item_id).first()
    items = VendorItem.query.filter_by(house_item_id=house_item_id).all()
    if house_item and items:
        for item in items:
            temp_price = float(item.price)
            if temp_price < lowest_price:
                lowest_price = temp_price
                item_id = item.id
            house_item.default_vendor_item_id = item_id
        db.session.commit()
        return jsonify('Default vendor item set!'), 200
    else:
        return jsonify('House item not found.'), 404


@api_bp.route('/login', methods=['GET'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message='Login succeeded.', access_token=access_token)
    else:
        return jsonify(message='Entered a bad email/password'), 401


@api_bp.route('/house_orders', methods=['GET'])
# @jwt_required()
def house_orders():
    orders_list = HouseOrder.query.order_by(HouseOrder.date).all()
    if orders_list:
        result = house_orders_schema.dump(orders_list)
        return jsonify(result), 200
    else:
        return jsonify('No house orders found.'), 404


@api_bp.route('/order_items/<int:order_id>', methods=['GET'])
# @jwt_required()
def order_items(order_id: int):
    items_list = HouseOrderItem.query.filter_by(HouseOrderItem.house_order_id == order_id). \
        order_by(HouseOrderItem.house_item.name).all()
    if items_list:
        result = house_order_items_schema.dump(items_list)
        return jsonify(result), 200
    else:
        return jsonify('No order items found.'), 404


@api_bp.route('/active_order', methods=['GET'])
# @jwt_required()
def active_order():
    order = HouseOrder.query.filter_by(HouseOrder.submitted is False).first()
    if order:
        item_list = HouseOrderItem.query.filter_by(HouseOrderItem.house_order_id == order.id).all()
        result = house_order_items_schema.dump(item_list)
        return jsonify(result), 200
    else:
        # create new set of house_order_items from active house_items
        # set of house_items and set house_order_id as order_id
        order = HouseOrder(date=DateTime(func.now()), submitted=False)
        house_item_list = HouseItem.query.filter_by(active=True).order_by(HouseItem.item_class).all()
        for item in house_item_list:
            new_order_item = HouseOrderItem(house_item_id=item.id, house_order_id=order.id, quantity=0)
            db.session.add(new_order_item)

        db.session.commit()
        item_list = HouseOrderItem.query.filter_by(HouseOrderItem.house_order_id == order.id).all()
        result = house_order_items_schema.dump(item_list)
        return jsonify(result), 200


@api_bp.route('/vendor_orders/<int:vendor_id>', methods=['GET'])
# @jwt_required()
def vendor_orders(vendor_id: int):
    orders = VendorOrder.query.filter_by(VendorOrder.vendor_id == vendor_id).order_by(VendorOrder.date).all()
    if orders:
        result = vendor_order_schema.dump(orders)
        return jsonify(result), 200
    else:
        return jsonify('No orders found for this vendor.'), 404


@api_bp.route('/house_inventory/<int:inventory_id>', methods=['GET'])
# @jwt_required()
def house_inventory(inventory_id: int):
    inventory = HouseInventory.query.filter_by(HouseInventory.id == inventory_id)
    if inventory:
        result = HouseInventorySchema.dump(inventory)
        return jsonify(result), 200
    else:
        return jsonify('No inventory found'), 404


@api_bp.route('/house_inventories', methods=['GET'])
# @jwt_required()
def house_inventories():
    inventories = HouseInventory.query.order_by(HouseInventory.date).all()
    if inventories:
        result = house_inventorys_schema.dump(inventories)
        return jsonify(result), 200
    else:
        return jsonify('No inventories found.'), 404


# TODO: Need to order by storage_location, item_class, and name
@api_bp.route('/house_inventory_items/<int:inventory_id>', methods=['GET'])
# @jwt_required()
def house_inventory_items(inventory_id: int):
    inventory_items = HouseInventoryItem.query.filter_by(HouseInventoryItem.house_inventory_id == inventory_id).all()
    if inventory_items:
        result = house_inventory_items_schema.dump(inventory_items)
        return jsonify(result), 200
    else:
        return jsonify('No inventory items found!'), 404


@api_bp.route('/active_inventory', methods=['GET'])
# @jwt_required()
def active_inventory():
    inventory = HouseInventory.query.filter_by(HouseInventory.submitted is False).first()
    if inventory:
        item_list = HouseInventoryItem.query.filter_by(HouseInventoryItem.house_inventory_id == inventory.id).all()
        result = house_inventory_items_schema.dump(item_list)
        return jsonify(result), 200
    else:
        # create new set of house_inventory_items from active house_items
        # set of house_items and set house_inventory_id as inventory_id
        inventory = HouseInventory(date=DateTime(func.now()), submitted=False)
        house_item_list = HouseItem.query.filter_by(active=True).order_by(HouseItem.item_class).all()
        for item in house_item_list:
            new_order_item = HouseInventoryItem(house_item_id=item.id, house_order_id=inventory.id, quantity=0)
            db.session.add(new_order_item)

        db.session.commit()
        item_list = HouseInventoryItem.query.filter_by(HouseInventoryItem.house_inventory_id == inventory.id).all()
        result = house_inventory_items_schema.dump(item_list)
        return jsonify(result), 200


@api_bp.route('/vendor_invoices/<int:vendor_id>', methods=['GET'])
# @jwt_required()
def vendor_invoices(vendor_id: int):
    invoices = VendorInvoice.query.filter_by(VendorInvoice.vendor_id == vendor_id).order_by(VendorInvoice.date)
    if invoices:
        result = vendor_invoice_schema.dump(invoices)
        return jsonify(result), 200
    else:
        return jsonify('No invoices found for this vendor!'), 404


@api_bp.route('/vendors', methods=['GET'])
# @jwt_required()
def vendors():
    vendor_objs = Vendor.query.all()
    if vendor_objs:
        result = vendors_schema.dump(vendor_objs)
        return jsonify(result), 200
    else:
        return jsonify('No vendors!'), 404


@api_bp.route('/vendor_items/<int:vendor_id>', methods=['GET'])
# @jwt_required()
def vendor_items(vendor_id: int):
    vendor = Vendor.query.filter_by(id=vendor_id).first()
    if vendor:
        result = vendor_items_schema.dump(vendor.vendor_items)
        return jsonify(result), 200
    else:
        return jsonify('No vendor items found.'), 404


@api_bp.route('/house_items', methods=['GET'])
# jwt_required
def house_items():
    items = db.session.query(HouseItem).filter(active=True).all()
    if items and items.size() > 0:
        result = house_items_schema.dump(items)
        return jsonify(result), 200
    else:
        return jsonify('No active house items found.'), 404


@api_bp.route('/get_storage_location_items/<int:location_id>', methods=['GET'])
# @jwt_required()
def house_items_storage_location(location_id: int):
    location = db.session.query(StorageLocation).filter_by(id=location_id).one()
    if location:
        if location.house_items:
            result = location_items_schema.dump(location.house_items)
            return jsonify(result), 200
        else:
            return jsonify('No items for location found.'), 404

    else:
        return jsonify('Location not found.'), 404


@api_bp.route('/add_vendor_item', methods=['POST'])
@jwt_required()
def add_vendor_item():
    vendor_id = request.form['vendor_id']
    vendor_product_id = request.form['vendor_product_id']
    test = VendorItem.query.filter_by(vendor_id=vendor_id, vendor_product_id=vendor_product_id)
    if test:
        return jsonify('Vendor item already in database.'), 401
    else:
        product_name = request.form['product_name']
        pack_size = request.form['pack_size']
        unit = request.form['unit']
        price = request.form['price']
        house_item_id = request.form['house_item_id']
        new_vendor_item = VendorItem(vendor_id=vendor_id, vendor_product_id=vendor_product_id,
                                     product_name=product_name, pack_size=pack_size, unit=unit,
                                     price=price, house_item_id=house_item_id)
        db.session.add(new_vendor_item)
        db.session.commit()
        return jsonify('Vendor item successfully added to database.'), 201


@api_bp.route('/add_house_item', methods=['POST'])
# @jwt_required()
def add_house_item():
    product_name = request.form['product_name']
    test = db.session.query(HouseItem).filter_by(name=product_name).first()
    if test:
        return jsonify('House item already in database.'), 401
    else:
        storage_location = request.form['storage_location']
        # inventory_category = request.form['inventory_category']
        # par = request.form['par']
        # have = request.form['have']
        active = True
        measure_unit = request.form['measure_unit']
        description = request.form['description']
        item_class_name = request.form['item_class_name']
        item_class = db.session.query(ItemClassification).filter_by(type=item_class_name).first()
        item_class_id = item_class.id
        storage_location_data = db.session.query(StorageLocation).filter_by(name=storage_location).first()
        new_house_item = HouseItem(name=product_name, description=description,
                                   measure_unit=measure_unit, active=active, item_class=item_class)
        # new_house_item.item_class_id = item_class_id
        if storage_location_data:
            new_house_item.storage_locations.append(storage_location)
        db.session.add(new_house_item)
        db.session.commit()
        return jsonify('House item successfully added to database'), 201


# TODO: add_vendor_invoice(): takes in vendor_id and invoice file, creates vendor_invoice object
@api_bp.route('/add_vendor_invoice', methods=['POST'])
# @jwt_required()
def add_vendor_invoice():
    vendor_id = request.form['vendor_id']
    vendor_order_id = request.form['vendor_order_id']
    date = request.form['date']
    invoice = VendorInvoice(vendor_id=vendor_id, vendor_order_id=vendor_order_id, date=date)
    db.session.add(invoice)
    db.session.commit()
    return jsonify('Vendor invoice successfully added to database.'), 201


# TODO: add_vendor(): creates new vendor object


@api_bp.route('/update_order_item_price/<int:order_item_id>/<string:price>', methods=['PUT'])
@jwt_required()
def update_order_item_price(order_item_id: int, price: str):
    item = HouseOrderItem.query.filter_by(id=order_item_id).first()
    if item:
        item.price = price
        db.session.commit()
        return jsonify('Vendor item price updated.'), 200
    else:
        return jsonify('Vendor item not found.'), 404


@api_bp.route('/update_order_item_quantity/<int:order_item_id>/<int:quantity>', methods=['PUT'])
@jwt_required()
def update_order_item_quantity(order_item_id: int, quantity: int):
    item = HouseOrderItem.query.filter_by(id=order_item_id).first()
    if item:
        item.quantity = quantity
        db.session.commit()
        return jsonify('Vendor item quantity updated.'), 200
    else:
        return jsonify('Vendor item not found.'), 404


@api_bp.route('/update_inventory_item_price/<int:inventory_item_id>/<string:price>', methods=['PUT'])
@jwt_required()
def update_inventory_item_price(inventory_item_id: int, price: str):
    item = HouseOrderItem.query.filter_by(id=inventory_item_id).first()
    if item:
        item.price = price
        db.session.commit()
        return jsonify('Vendor item price updated.'), 200
    else:
        return jsonify('Vendor item not found.'), 404


@api_bp.route('/update_inventory_item_quantity/<int:inventory_item_id>/<int:quantity>', methods=['PUT'])
@jwt_required()
def update_inventory_item_quantity(inventory_item_id: int, quantity: int):
    item = HouseOrderItem.query.filter_by(id=inventory_item_id).first()
    if item:
        item.quantity = quantity
        db.session.commit()
        return jsonify('Vendor item quantity updated.'), 200
    else:
        return jsonify('Vendor item not found.'), 404


# TODO: update_house_item()'s
@api_bp.route('/add_house_item_storage_location/<int:house_item_id>/<int:storage_loc>', methods=['PUT'])
# @jwt_required()
def add_house_item_storage_location(house_item_id: int, storage_loc: int):
    item = db.session.query(HouseItem).filter_by(id=house_item_id).first()
    location = db.session.query(StorageLocation).filter_by(id=storage_loc).first()
    if item and location:
        item.storage_locations.append(location)
        db.session.commit()
        return jsonify('Storage location added to house item'), 200
    else:
        return jsonify('Unable able to add house item to location.'), 404


@api_bp.route('/set_default_vendor_item/<int:house_item_id>', methods=['PUT'])
@jwt_required()
def set_default_vendor_item(house_item_id: int):
    item = HouseItem.query.filter_by(id=house_item_id).first()
    if item:
        set_default_vendor_item_helper(item.id)
        return jsonify('Default vendor item set.'), 200

    else:
        return jsonify('House item not found. Default vendor item not set.'), 404


@api_bp.route('/set_default_vendor_items', methods=['PUT'])
@jwt_required()
def set_default_vendor_items():
    items = HouseItem.query.all()
    if items:
        for item in items:
            set_default_vendor_item_helper(item.id)

        return jsonify('Default vendor items set.'), 200
    else:
        return jsonify('No house items found.'), 404


@api_bp.route('/remove_vendor_item/<int:vendor_item_id>/', methods=['PUT'])
@jwt_required()
def deactivate_vendor_item(vendor_item_id: int):
    item = VendorItem.query.filter_by(id=vendor_item_id).first()
    if item:
        item.active = False
        db.session.commit()
        return jsonify('Vendor item inactivated.'), 202
    else:
        return jsonify('Vendor item doesn\'t exist.'), 404


@api_bp.route('/remove_house_item/<int:house_item_id>', methods=['PUT'])
@jwt_required()
def deactivate_house_item(house_item_id: int):
    item = HouseItem.query.filter_by(id=house_item_id).first()
    if item:
        item.active = False
        db.session.commit()
        return jsonify('House item inactivated.'), 202
    else:
        return jsonify('House item doesn\'t exist.')
