from flask import jsonify, Blueprint
from sqlalchemy import DateTime, func
from src.model import *

blueprint_inventories = Blueprint('inventories_bp', __name__)


@blueprint_inventories.route('/get_inventory/<int:inventory_id>', methods=['GET'])
# @jwt_required()
def house_inventory(inventory_id: int):
    inventory = HouseInventory.query.filter_by(HouseInventory.id == inventory_id)
    if inventory:
        result = HouseInventorySchema.dump(inventory)
        return jsonify(result), 200
    else:
        return jsonify('No inventory found'), 404


@blueprint_inventories.route('/get_inventories', methods=['GET'])
# @jwt_required()
def house_inventories():
    inventories = HouseInventory.query.order_by(HouseInventory.date).all()
    if inventories:
        result = house_inventorys_schema.dump(inventories)
        return jsonify(result), 200
    else:
        return jsonify('No inventories found.'), 404


# TODO: Need to order by storage_location, item_class, and name
@blueprint_inventories.route('/get_inventory_items/<int:inventory_id>', methods=['GET'])
# @jwt_required()
def house_inventory_items(inventory_id: int):
    inventory_items = HouseInventoryItem.query.filter_by(HouseInventoryItem.house_inventory_id == inventory_id).all()
    if inventory_items:
        result = house_inventory_items_schema.dump(inventory_items)
        return jsonify(result), 200
    else:
        return jsonify('No inventory items found!'), 404


@blueprint_inventories.route('/get_active_inventory', methods=['GET'])
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


@blueprint_inventories.route('/update_inventory_item_price/<int:inventory_item_id>/<string:price>', methods=['PUT'])
# @jwt_required()
def update_inventory_item_price(inventory_item_id: int, price: str):
    item = HouseOrderItem.query.filter_by(id=inventory_item_id).first()
    if item:
        item.price = price
        db.session.commit()
        return jsonify('Vendor item price updated.'), 200
    else:
        return jsonify('Vendor item not found.'), 404


@blueprint_inventories.route('/update_inventory_item_quantity/<int:inventory_item_id>/<int:quantity>', methods=['PUT'])
# @jwt_required()
def update_inventory_item_quantity(inventory_item_id: int, quantity: int):
    item = HouseOrderItem.query.filter_by(id=inventory_item_id).first()
    if item:
        item.quantity = quantity
        db.session.commit()
        return jsonify('Vendor item quantity updated.'), 200
    else:
        return jsonify('Vendor item not found.'), 404