import sqlite3
from flask_restful import Resource, reqparse
import hmac
from flask_jwt_extended import create_access_token
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = "'This field cannot be blank."
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = "'This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(query, (data['username'], data['password']))
        # connection.commit()
        # connection.close()
        
        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User created successfully.'}, 201

class UserLogin(Resource):
    user_parser = reqparse.RequestParser()
    user_parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank.")
    user_parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank.")

    def post(self):
        data = UserLogin.user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and hmac.compare_digest(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid Credentials!'}, 401