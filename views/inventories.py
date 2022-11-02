from extensions.api import Blueprint, SQLCursorPage
from sqlalchemy import DateTime
from models.model import HouseInventory, HouseInventoryItem, HouseItem, HouseOrderItem
from models.schema import HouseInventorySchema, HouseInventoryItemSchema
from flask.views import MethodView
from extensions.database import db


blp = Blueprint('house_inventories', __name__, url_prefix='/inventory', description='Operations on House Inventories')


@blp.route('/')
class HouseInventories(MethodView):
    @blp.response(200, HouseInventorySchema(many=True))
    def get(self):
        """
        List All HouseInventory's
        """
        inventories = HouseInventory.query.all()
        return inventories

    @blp.arguments(HouseInventorySchema)
    @blp.response(201, HouseInventorySchema)
    def post(self, new_item):
        """
        Add new HouseInventory
        """
        inv = HouseInventory(**new_item)
        db.session.add(inv)
        db.session.commit()
        house_items = HouseItem.query.filter(HouseItem.active is True).all()
        for item in house_items:
            new_inv_item = HouseInventoryItemSchema(
                house_item_id=item.id,
                house_inventory_id=inv.id,
                date=inv.date,
                quantity='0',
                measure_unit=item.measure_unit,
                price=item.cur_price
            )
            db.session.add(new_inv_item)
        db.session.commit()
        return inv


@blp.route('/<int:inventory_id>')
class HouseInventory(MethodView):
    @blp.response(200, HouseInventorySchema)
    def get(self, inventory_id):
        """
        Get HouseInventory by id
        """
        inventory = HouseInventory.query.get_or_404(inventory_id)
        return inventory

    @blp.etag
    @blp.arguments(HouseInventorySchema)
    @blp.response(200, HouseInventorySchema)
    def put(self, update_data, inventory_id):
        """
        Update HouseInventory by id
        """
        inventory = HouseInventory.get_or_404(inventory_id)
        blp.check_etag(inventory, HouseInventorySchema)
        HouseInventory().update(inventory, update_data)
        db.session.add(inventory)
        db.session.commit()


@blp.route('/<int:inventory_id>/inventory_items')
class HouseInventoryItems(MethodView):
    @blp.response(200, HouseInventoryItemSchema(many=True))
    def get(self, sort_params, inventory_id):
        """
        Get list HouseInventoryItem's by inventory id
        """
        inventory_items = HouseInventoryItem.query.filter(HouseInventoryItem.house_inventory_id == inventory_id).order_by(sort_params).all()
        return inventory_items


@blp.route('/inventory_item/<int:inventory_item_id>')
class InventoryItem(MethodView):
    @blp.response(200, HouseInventoryItemSchema)
    def get(self, inventory_item_id):
        """
        Get HouseInventoryItem by id
        """
        return HouseInventoryItem.get_or_404(inventory_item_id)

    @blp.etag
    @blp.arguments(HouseInventoryItemSchema)
    @blp.response(200, HouseInventoryItemSchema)
    def put(self, update_data, inventory_item_id):
        """
        Update HouseInventoryItem
        """
        item = HouseOrderItem.get_or_404(inventory_item_id)
        blp.check_etag(item, HouseInventoryItemSchema)
        HouseInventoryItem().update(item, update_data)
        db.session.add(item)
        db.session.commit()
        return item


@blp.route('/active_inventory')
class ActiveInventory(MethodView):
    @blp.response(200, HouseInventorySchema)
    def get(self):
        """
        Get active HouseInventory or create new
        """
        inventory = HouseInventory.query.filter_by(HouseInventory.submitted is False).first()
        if inventory:
            return HouseInventoryItem.query.filter_by(HouseInventoryItem.house_inventory_id == inventory.id).all()
        else:
            # create new set of house_inventory_items from active house_items
            # set of house_items and set house_inventory_id as inventory_id
            inventory = HouseInventory(
                date=DateTime.now(),
                submitted=False,
            )
            db.session.add(inventory)
            house_items = HouseItem.query.filter(HouseItem.active is True).all()
            for item in house_items:
                new_inv_item = HouseInventoryItemSchema(
                    house_item_id=item.id,
                    house_inventory_id=inventory.id,
                    date=inventory.date,
                    quantity='0',
                    measure_unit=item.measure_unit,
                    price=item.cur_price
                )
                db.session.add(new_inv_item)
            db.session.commit()
            return inventory
