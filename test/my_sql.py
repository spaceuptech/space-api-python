from space_api import API, COND

api = API('grpc', 'localhost:8081')
api.set_token('my_secret')
db = api.my_sql()

# testing
print(db.delete('books').apply())

# insert - 2/2 passing
# all
print(db.insert('books').docs([{"name": "BookName"}, {"name": "BookName"}]).apply())
# one
print(db.insert('books').doc({"name": "MyBook", "author": "John Doe"}).apply())

# get - 12/12 passing
# all
print(db.get('books').apply())
# one
print(db.get_one('books').apply())
# limit all
print(db.get('books').limit(2).apply())
# limit one
print(db.get_one('books').limit(2).apply())
# skip all
print(db.get('books').skip(2).apply())
# skip one
print(db.get_one('books').skip(2).apply())
# sort all
print(db.get('books').sort('-author').apply())
# sort one
print(db.get_one('books').sort('author').apply())
# select all
print(db.get('books').select({'author': 1}).apply())
# select one
print(db.get_one('books').select({'author': 1}).apply())
# where all
print(db.get('books').where(COND("name", "==", "Book_name")).apply())
# where one
print(db.get_one('books').where(COND("name", "==", "BookName")).apply())

# update - 4/4 passing
# set all
print(db.update('books').set({"author": "myself"}).apply())
# set one
print(db.update_one('books').set({"author": "myself"}).apply())
# set where all
print(db.update('books').where(COND("author", "==", "some_author")).set({"author": "myself"}).apply())
# set where one
print(db.update_one('books').where(COND("author", "==", "some_author")).set({"author": "myself"}).apply())

# testing
print(db.get('books').apply())

# delete - 4/4 passing
# all
print(db.delete('books').apply())
# one
print(db.delete_one('books').apply())
# where, all
print(db.delete('books').where(COND('name', '!=', 'Book_name')).apply())
# where, one
print(db.delete_one('books').where(COND('name', '!=', 'Book_name')).apply())

# testing
print(db.get('books').apply())

api.close()
