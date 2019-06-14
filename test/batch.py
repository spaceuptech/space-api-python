from space_api import API, COND

api = API('grpc', 'localhost:8081')
api.set_token('my_secret')
db = api.my_sql()


b = db.begin_batch()
b.add(db.insert('books').doc({"name": "MyBook", "author": "John Doe"}))
b.add(db.insert('books').docs([{"name": "BookName"}, {"name": "BookName"}]))
b.add(db.delete('books').where(COND('name', '!=', 'Book_name')))
response = b.apply()
print(response)