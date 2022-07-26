from flask import jsonify, Blueprint
from sqlalchemy import DateTime, func
from src.model import *
from src.schema import *


blueprint_house_orders = Blueprint('house_orders_bp', __name__)


@blueprint_house_orders.route('/orders', methods=['GET'])
# @jwt_required()
def house_orders():
    orders_list = HouseOrder.query.order_by(HouseOrder.date).all()
    if orders_list:
        result = house_orders_schema.dump(orders_list)
        return jsonify(result), 200
    else:
        return jsonify('No house orders found.'), 404


@blueprint_house_orders.route('/order_items/<int:order_id>', methods=['GET'])
# @jwt_required()
def order_items(order_id: int):
    items_list = HouseOrderItem.query.filter_by(HouseOrderItem.house_order_id == order_id). \
        order_by(HouseOrderItem.house_item.name).all()
    if items_list:
        result = house_order_items_schema.dump(items_list)
        return jsonify(result), 200
    else:
        return jsonify('No order items found.'), 404


@blueprint_house_orders.route('/active_order', methods=['GET'])
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


@blueprint_house_orders.route('/order_item_price/<int:order_item_id>/<string:price>', methods=['PUT'])
# @jwt_required()
def update_order_item_price(order_item_id: int, price: str):
    item = HouseOrderItem.query.filter_by(id=order_item_id).first()
    if item:
        item.price = price
        db.session.commit()
        return jsonify('Vendor item price updated.'), 200
    else:
        return jsonify('Vendor item not found.'), 404


@blueprint_house_orders.route('/order_item_quantity/<int:order_item_id>/<int:quantity>', methods=['PUT'])
# @jwt_required()
def update_order_item_quantity(order_item_id: int, quantity: int):
    item = HouseOrderItem.query.filter_by(id=order_item_id).first()
    if item:
        item.quantity = quantity
        db.session.commit()
        return jsonify('Vendor item quantity updated.'), 200
    else:
        return jsonify('Vendor item not found.'), 404

