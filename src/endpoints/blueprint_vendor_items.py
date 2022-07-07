from flask import request, jsonify, Blueprint
from src.model import *

blueprint_vendor_items = Blueprint('vendor_items_bp', __name__)


@blueprint_vendor_items.route('/get_items/<int:vendor_id>', methods=['GET'])
# @jwt_required()
def vendor_items(vendor_id: int):
    vendor = Vendor.query.filter_by(id=vendor_id).first()
    if vendor:
        result = vendor_items_schema.dump(vendor.vendor_items)
        return jsonify(result), 200
    else:
        return jsonify('No vendor items found.'), 404


@blueprint_vendor_items.route('/add_item', methods=['POST'])
# @jwt_required()
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


@blueprint_vendor_items.route('/set_default_item/<int:house_item_id>', methods=['PUT'])
# @jwt_required()
def set_default_vendor_item(house_item_id: int):
    item = HouseItem.query.filter_by(id=house_item_id).first()
    if item:
        set_default_vendor_item_helper(item.id)
        return jsonify('Default vendor item set.'), 200

    else:
        return jsonify('House item not found. Default vendor item not set.'), 404


@blueprint_vendor_items.route('/set_default_items', methods=['PUT'])
# @jwt_required()
def set_default_vendor_items():
    items = HouseItem.query.all()
    if items:
        for item in items:
            set_default_vendor_item_helper(item.id)

        return jsonify('Default vendor items set.'), 200
    else:
        return jsonify('No house items found.'), 404


@blueprint_vendor_items.route('/remove_item/<int:vendor_item_id>/', methods=['PUT'])
# @jwt_required()
def deactivate_vendor_item(vendor_item_id: int):
    item = VendorItem.query.filter_by(id=vendor_item_id).first()
    if item:
        item.active = False
        db.session.commit()
        return jsonify('Vendor item inactivated.'), 202
    else:
        return jsonify('Vendor item doesn\'t exist.'), 404