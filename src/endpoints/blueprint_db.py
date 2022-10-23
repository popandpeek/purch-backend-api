import datetime

from flask import request, jsonify, Blueprint
from sqlalchemy import DateTime, func
from src.model import *


blueprint_db = Blueprint('blueprint_db', __name__)


@blueprint_db.cli.command('db_create')
def db_create():
    db.create_all()
    db.session.commit()


@blueprint_db.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("Database dropped.")


@blueprint_db.cli.command('db_seed')
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
        measure_unit='pound'
    )
    v_order_item2 = VendorOrderItem(
        price='0.82',
        quantity='40',
        measure_unit='pound'
    )
    v_order_item3 = VendorOrderItem(
        price='0.54',
        quantity='80',
        measure_unit='pound'
    )

    # HOUSE_ORDER_ITEMS
    order_item1 = HouseOrderItem(
        quantity='40',
        measure_unit='pound',
        vendor_order_item=v_order_item1
    )
    order_item2 = HouseOrderItem(
        quantity='40',
        measure_unit='pound',
        vendor_order_item=v_order_item2
    )
    order_item3 = HouseOrderItem(
        quantity='80',
        measure_unit='pound',
        vendor_order_item=v_order_item3
    )

    # HOUSE INVENTORY ITEMS
    house_inventory_item1 = HouseInventoryItem(
        date=datetime.datetime(2020, 9, 30),
        quantity='27',
        measure_unit='pound',
        price='0.65',
    )
    house_inventory_item2 = HouseInventoryItem(
        date=datetime.datetime(2020, 9, 30),
        quantity='12',
        measure_unit='pound',
        price='0.78',
    )

    # HOUSE ORDERS
    order1 = HouseOrder(
        date=datetime.datetime(2020, 9, 18),
        submitted=True,
        house_order_items=[order_item1, order_item2]
    )
    order2 = HouseOrder(
        date=datetime.datetime(2020, 9, 28),
        submitted=True,
        house_order_items=[order_item3]
    )

    # VENDOR ORDERS
    vendor_order1 = VendorOrder(
        date=datetime.datetime(2020, 9, 18),
        submitted=True,
        vendor_order_items=[v_order_item1],
    )
    vendor_order2 = VendorOrder(
        date=datetime.datetime(2020, 9, 18),
        submitted=True,
        vendor_order_items=[v_order_item2],
    )
    vendor_order3 = VendorOrder(
        date=datetime.datetime(2020, 9, 28),
        submitted=True,
        vendor_order_items=[v_order_item3],
    )

    # HOUSE INVENTORIES
    house_inventory = HouseInventory(
        date=datetime.datetime(2020, 9, 30),
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

    # VENDOR INVOICE ITEMS
    vendor_inv_item1 = VendorInvoiceItem(
        measure_unit='pound',
        pack_size=40,
        pack_number=1,
        price='0.55',
        quantity='40'
    )
    vendor_inv_item2 = VendorInvoiceItem(
        measure_unit='pound',
        pack_size=1,
        pack_number=40,
        price='0.82',
        quantity='40'
    )
    vendor_inv_item3 = VendorInvoiceItem(
        measure_unit='pound',
        pack_size=40,
        pack_number=1,
        price='80',
        quantity='0.54'
    )

    # VENDOR INVOICES
    vendor_invoice1 = VendorInvoice(
        date=datetime.datetime(2020, 9, 18),
        vendor_order=vendor_order1,
        vendor_invoice_items=[vendor_inv_item1, vendor_inv_item2],
        paid=False
    )
    vendor_invoice2 = VendorInvoice(
        date=datetime.datetime(2020, 9, 18),
        vendor_order=vendor_order2,
        vendor_invoice_items=[vendor_inv_item3],
        paid=False
    )

    # VENDOR ITEMS
    carrots_vendor1 = VendorItem(
        vendor_SKU='444465354654',
        active=True,
        vendor_product_id=123,
        product_name='Carrots, raw',
        description='Bulk carrots, 40#',
        measure_unit='pound',
        pack_size=40,
        pack_number=1,
        brand_name='Thumper',
        vendor_order_items=[v_order_item3],
        vendor_invoice_items=[vendor_inv_item3]
    )
    potato_vendor = VendorItem(
        vendor_SKU='5630785467',
        active=True,
        vendor_product_id=8765,
        product_name='Potatoes, #2',
        description='Best bakers',
        measure_unit='pound',
        pack_size=1,
        pack_number=40,
        brand_name='Idaho Spuds',
        vendor_order_items=[v_order_item2],
        vendor_invoice_items=[vendor_inv_item2]
    )
    carrots_vendor2 = VendorItem(
        vendor_SKU='63645689453',
        active=True,
        vendor_product_id=132,
        product_name='Carrots, raw',
        description='Bulk carrots, 40#',
        measure_unit='pound',
        pack_size=40,
        pack_number=1,
        brand_name='Sunshine',
        vendor_order_items=[v_order_item1],
        vendor_invoice_items=[vendor_inv_item1]
    )

    # HOUSE ITEMS
    carrots_house = HouseItem(
        name='carrots, raw, bulk',
        description='Carrots, bulk',
        active=True,
        measure_unit='pound',
        house_order_items=[order_item1, order_item3],
        house_inventory_items=[house_inventory_item1],
        vendor_items=[carrots_vendor1, carrots_vendor2],
        default_vendor_item_id=None,
        storage_locations=[kitchen_dry_storage],
        item_class=produce
    )
    potato_house = HouseItem(
        name='potato, #2, raw',
        description='#2 Bakers, bulk',
        active=True,
        measure_unit='pound',
        house_order_items=[order_item2],
        house_inventory_items=[house_inventory_item2],
        vendor_items=[potato_vendor],
        default_vendor_item_id=None,
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
        vendor_invoices=[vendor_invoice1]
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

    # HOUSE_ORDER_ITEMS
    db.session.add(order_item1)
    db.session.add(order_item2)
    db.session.add(order_item3)

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

    # VENDOR_INVOICE_ITEMS
    db.session.add(vendor_inv_item1)
    db.session.add(vendor_inv_item2)
    db.session.add(vendor_inv_item3)

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
