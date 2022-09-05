from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'my secret key'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True,
        help = 'This field cannot be left blank!'
    )    

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()
        # data = request.get_json(silent=True, force=True)
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 # create

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>') # http://localhost:5000/item/<name>
api.add_resource(ItemList, '/items')

stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
            'name': 'My Item',
            'price': 15.99
            }
        ]
    }
]

@app.route('/')
def home():
    return render_template('index.html')

# POST /store data: {name:}
@app.route('/store', methods=["POST"])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>') # 'http://127.0.0.1:5000/store/some_name'
def get_store(name):
    # iterate over stores, if the store name matches, return it, if not, return error message
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found!'}) 

# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})

# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def post_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found!'})

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found!'}) 

app.run(port=5000, debug=True)