from space_api import API, AND, OR, COND

api = API('grpc', 'localhost:8081')
api.set_token('my_secret')
db = api.my_sql()

# insert - 2/2 passing
# one
print(db.insert('books').one({"name": "MyBook", "author": "John Doe"}))
# all
print(db.insert('books').all([{"name": "BookName"}, {"name": "BookName"}]))

# delete - 2/2 passing
# all
print(db.delete('books').all())
# where, all
print(db.delete('books').where(COND('name', '!=', 'Book_name')).all())

# get - 12/12 passing
# all
print(db.get('books').all())
# one
print(db.get('books').one())
# limit all
print(db.get('books').limit(2).all())
# limit one
print(db.get('books').limit(2).one())
# skip all
print(db.get('books').skip(2).all())
# skip one
print(db.get('books').skip(2).one())
# sort all
print(db.get('books').sort('-author').all())
# sort one
print(db.get('books').sort('author').one())
# select all
print(db.get('books').select({'author': 1}).all())
# select one
print(db.get('books').select({'author': 1}).one())
# where all
print(db.get('books').where(COND("name", "==", "Book_name")).all())
# where one
print(db.get('books').where(COND("name", "==", "BookName")).one())


# update - 2/2 passing
# set all
print(db.update('books').set({"author": "myself"}).all())
# set where all
print(db.update('books').where(COND("author", "==", "some_author")).set({"author": "myself"}).all())

# testing
print(db.get('books').all())

api.close()
