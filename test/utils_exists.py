import jwt
from space_api import API

api = API('books-app', 'localhost:4124')
db = api.my_sql()
api.set_token(jwt.encode({"password": "super_secret_admin_password"}, 'my_secret', algorithm='HS256').decode('utf-8'))

print(db.get('books').apply())