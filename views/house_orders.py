from extensions.api import Blueprint, SQLCursorPage
from flask.views import MethodView
from sqlalchemy import DateTime, func
from models.model import HouseOrder, HouseOrderItem, HouseItem
from models.schema import HouseOrderSchema, HouseOrderItemSchema
from extensions.database import db


blp = Blueprint('house_orders', __name__, url_prefix='/house_orders', description='Operations on House Orders')


@blp.route('/')
# @jwt_required()
class HouseOrders(MethodView):
    @blp.response(200, HouseOrderSchema(many=True))
    def get(self):
        """
        List all HouseOrders
        """
        orders_list = HouseOrder.query.order_by(HouseOrder.date)
        return orders_list

    @blp.arguments(HouseOrderSchema)
    @blp.response(201, HouseOrderSchema)
    def post(self, new_data):
        """
        Create new HouseOrder
        """
        order = HouseOrder.create(**new_data)
        db.session.add(order)
        db.session.commit()
        return order

    @blp.etag
    @blp.arguments(HouseOrderSchema)
    @blp.response(200, HouseOrderSchema)
    def put(self, update_data, order_id):
        """
        Updates HouseOrder
        """
        order = HouseOrder.query.get_or_404(order_id)
        blp.check_etag(order, HouseOrderSchema)
        HouseOrderSchema().update(order, update_data)
        db.session.add(order)
        db.session.commit()
        return order


@blp.route('/<int:order_id>')
class HouseOrderItems(MethodView):
    @blp.response(200, HouseOrderItemSchema(many=True))
    def get(self, order_id):
        """
        Gets HouseOrder by order id
        """
        order = HouseOrder.query.get_or_404(order_id)
        return order.house_order_items


@blp.route('/active_order')
class ActiveOrder(MethodView):
    @blp.response(200, HouseOrderSchema())
    def get(self):
        """
        Get active orders list of HouseOrderItems
        """
        order = HouseOrder.query.filter_by(HouseOrder.submitted is False).first()
        if order:
            return HouseOrderItem.query.filter_by(HouseOrderItem.house_order_id == order.id).all()
        else:
            # create new set of house_order_items from active house_items
            # set of house_items and set house_order_id as order_id
            order = HouseOrder(date=DateTime(func.now()), submitted=False)
            house_item_list = HouseItem.query.filter_by(active=True).order_by(HouseItem.item_class).all()
            for item in house_item_list:
                new_order_item = HouseOrderItem(house_item_id=item.id, house_order_id=order.id, quantity=0)
                db.session.add(new_order_item)

            db.session.add(order)
            db.session.commit()
            return order


@blp.route('/active_order/<string:item_id>')
class ActiveOrderItems(MethodView):
    @blp.response(200, HouseOrderItemSchema)
    def get(self, item_id):
        """
        Get HouseOrderItem from active order by HouseOrderItem id
        """
        item = HouseOrderItem.query.get_or_404(item_id)
        return item

    @blp.arguments(HouseOrderItemSchema, location='json')
    @blp.response(200, HouseOrderItemSchema)
    def put(self, new_item, item_id):
        """
        Updates HouseOrderItem
        """
        item = HouseOrderItem.query.get_or_404(item_id)
        HouseOrderItemSchema().update(item, new_item)
        db.session.commit()
        return item
