import time
from space_api import API, COND

api = API('grpc', 'localhost:8081')
db = api.my_sql()
initial = 3
print(db.get('books').apply().result)
print("Delete all", db.delete('books').apply())

i = initial
while True:
    print("Insert", db.insert('books').doc({"id": i, "name": "MyBook" + str(i), "author": "Author" + str(i)}).apply())
    print(db.get('books').apply().result)
    time.sleep(3)
    print("Update", db.update('books').set({"author": "myself" + str(i)}).where(COND("id", "==", i)).apply())
    print(db.get('books').apply().result)
    time.sleep(3)
    print("Delete", db.delete_one('books').where(COND("id", "==", i)).apply())
    print(db.get('books').apply().result)
    time.sleep(4)
    i += 1

api.close()
