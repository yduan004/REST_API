import hmac
from user import User

users = [
    User(1, 'bob', 'asdf')
]

username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and hmac.compare_digest(user.password, password):
        return user

def identity(payload):
    user_id = payload['identify']
    return userid_mapping.get(user_id, None)