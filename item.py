import sqlite3
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True,
        help = 'This field cannot be left blank!'
    )    

    @jwt_required()
    def get(self, name):
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return {'item': item}, 200 if item else 404
        item = self.find_by_name(name)
        return item if item else {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        # if next(filter(lambda x: x['name'] == name, items), None):
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400 # bad request

        data = Item.parser.parse_args()
        # data = request.get_json(silent=True, force=True)
        item = {'name': name, 'price': data['price']}
        # items.append(item)
        try:
            self.insert(item)
        except:
            return {'message': 'An error occurred inserting the item.'}, 500 # Internal Server Error
        return item, 201 # create

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}

    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # if item is None:
        #     item = {'name': name, 'price': data['price']}
        #     items.append(item)
        # else:
        #     item.update(data)
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {'message': 'An error occurred inserting the item.'}, 500
        else: 
            try:
                self.update(updated_item)
            except:
                return {'message': 'An error occurred updating the item.'}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

class ItemList(Resource):
    def get(self):
        # return {'items': items}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()
        return {'items': items}