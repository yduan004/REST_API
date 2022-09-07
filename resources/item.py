# import sqlite3
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask_restful import Resource, reqparse
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True,
        help = 'This field cannot be left blank!'
    )    
    parser.add_argument('store_id', 
        type=int, 
        required=True,
        help = 'Every item needs a store id!'
    )    

    @jwt_required()
    def get(self, name):
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return {'item': item}, 200 if item else 404
        item = ItemModel.find_by_name(name)
        if item: 
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required(fresh=True)
    def post(self, name):
        # if next(filter(lambda x: x['name'] == name, items), None):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400 # bad request

        data = Item.parser.parse_args()
        # data = request.get_json(silent=True, force=True)
        item = ItemModel(name, **data)
        # items.append(item)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500 # Internal Server Error
        return item.json(), 201 # create

    @jwt_required()
    def delete(self, name):
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))

        # connection.commit()
        # connection.close()
        # return {'message': 'Item deleted'}
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item delted.'}
        return {'message': 'Item not found'}, 404

    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # if item is None:
        #     item = {'name': name, 'price': data['price']}
        #     items.append(item)
        # else:
        #     item.update(data)
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()
        return item.json()

        # if item is None:
        #     try:
        #         updated_item.insert()
        #     except:
        #         return {'message': 'An error occurred inserting the item.'}, 500
        # else: 
        #     try:
        #         updated_item.update()
        #     except:
        #         return {'message': 'An error occurred updating the item.'}, 500
        # return updated_item.json()


class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {
            'items': [item['name'] for item in items],
            'message': 'More data available if you log in.'
        }, 200
        # return {'items': items}
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})
        # connection.close()
        # return {'items': items}
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}