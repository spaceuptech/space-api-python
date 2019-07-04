import time
from space_api import API, COND

api = API('books-app', 'localhost:8081')
db = api.my_sql()
initial = 3
print(db.get('books').apply().result)
print("Delete all", db.delete('books').apply())
print("Insert", db.insert('books').doc({"id": 0, "name": "MyBook" + str(0), "author": "Author" + str(0)}).apply())
print("Insert", db.insert('books').doc({"id": 1, "name": "MyBook" + str(1), "author": "Author" + str(1)}).apply())

i = initial
while True:
    print("Insert", db.insert('books').doc({"id": i, "name": "MyBook" + str(i), "author": "Author" + str(i)}).apply())
    print(db.get('books').apply().result)
    time.sleep(2)
    print("Update", db.update('books').set({"author": "myself" + str(i)}).where(COND("id", "==", i)).apply())
    print(db.get('books').apply().result)
    time.sleep(2)
    print("Delete", db.delete_one('books').where(COND("id", "==", i)).apply())
    print(db.get('books').apply().result)
    time.sleep(4)
    i += 1

api.close()
