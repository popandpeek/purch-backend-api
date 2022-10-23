from flask import request, jsonify, Blueprint, json
from http import HTTPStatus
from flasgger import swag_from
from src.model import *
from src.schema import HouseItemSchema, house_items_schema, StorageLocationSchema


blueprint_house_items = Blueprint('house_items_bp', __name__)


@blueprint_house_items.route('/items', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'House item GET request',
            'schema': HouseItemSchema
        }
    }
})
# jwt_required
def house_items():
    """
    This endpoint returns a list of all house items
    :return: json object
    """
    items = db.session.query(HouseItem).filter_by(active=True).all()
    if items is not None:
        result = house_items_schema.dumps(items)
        return jsonify(json.loads(result)), 200
    else:
        return jsonify('No active house items found.'), 404


@blueprint_house_items.route('/storage_location_items/<int:location_id>', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'House items in specified storage location GET request',
            'schema': StorageLocationSchema
        }
    }
})
# @jwt_required()
def house_items_storage_location(location_id: int):
    location = db.session.query(StorageLocation).filter_by(id=location_id).one()
    if location:
        if location.house_items:
            result = StorageLocationSchema.dumps(json.loads(location.house_items))
            return jsonify(result), 200
        else:
            return jsonify('No items for location found.'), 404

    else:
        return jsonify('Location not found.'), 404


@blueprint_house_items.route('/items', methods=['POST'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'House item POST request',
            'schema': HouseItemSchema
        }
    }
})
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
        storage_location_data = db.session.query(StorageLocation).filter_by(name=storage_location).first()
        new_house_item = HouseItem(name=product_name, description=description,
                                   measure_unit=measure_unit, active=active, item_class=item_class)
        if storage_location_data:
            new_house_item.storage_locations.append(storage_location)
        db.session.add(new_house_item)
        db.session.commit()
        return jsonify('House item successfully added to database'), 201


# TODO: update_house_item()'s
@blueprint_house_items.route('/item_storage_location/<int:item_id>/<int:storage_loc>', methods=['PUT'])
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


@blueprint_house_items.route('/deactivate_item/<int:house_item_id>', methods=['PUT'])
# @jwt_required()
def deactivate_house_item(house_item_id: int):
    item = HouseItem.query.filter_by(id=house_item_id).first()
    if item:
        item.active = False
        db.session.commit()
        return jsonify('House item inactivated.'), 202
    else:
        return jsonify('House item doesn\'t exist.')
