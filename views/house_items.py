from extensions.api import Blueprint, SQLCursorPage
from models.model import HouseItem, StorageLocation
from models.schema import HouseItemSchema, StorageLocationSchema
from flask.views import MethodView
from extensions.database import db


blp = Blueprint('house_items', __name__, url_prefix="/house_items", description="Operations on House Items")


@blp.route('/')
class HouseItems(MethodView):
    @blp.response(200, HouseItemSchema(many=True))
    def get(self):
        """
        List All HouseItems
        """
        items = HouseItem.query.all()
        return items

    @blp.arguments(HouseItemSchema)
    @blp.response(201, HouseItemSchema)
    def post(self, new_data):
        """
        Add HouseItem
        """
        item = HouseItem.create(**new_data)
        db.session.add(item)
        db.session.commit()
        return item


@blp.route("/<int:house_item_id>")
class HouseItemById(MethodView):
    @blp.response(200, HouseItemSchema)
    def get(self, house_item_id):
        """
        Get HouseItem
        """
        return HouseItem.query.get_or_404(house_item_id)

    @blp.etag
    @blp.arguments(HouseItemSchema)
    @blp.response(200, HouseItemSchema)
    def put(self, update_data, house_item_id):
        """
        Update HouseItem
        """
        item = HouseItem.query.get_or_404(house_item_id)
        blp.check_etag(item, HouseItemSchema)
        HouseItemSchema().update(item, update_data)
        db.session.add(item)
        db.session.commit()
        return item


@blp.route("/storage_locations/<string:storage_name>")
class HouseItemByStorageLocation(MethodView):
    @blp.arguments(StorageLocationSchema)
    @blp.response(200, HouseItemSchema(many=True))
    def get(self, storage_name):
        """
        Get HouseItems by storage location
        """
        items = StorageLocation.query.filter(StorageLocation.name == storage_name).all()
        return items

