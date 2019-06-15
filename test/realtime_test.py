import time
from space_api import API, COND

api = API('grpc', 'localhost:8081')
db = api.my_sql()
initial = 3
print(db.delete('books').apply())
for i in range(initial):
    print(db.insert('books').doc({"id": i, "name": "MyBook" + str(i), "author": "Author" + str(i)}).apply())

i = initial
while True:
    print(db.insert('books').doc({"id": i, "name": "MyBook" + str(i), "author": "Author" + str(i)}).apply())
    time.sleep(3)
    print(db.update('books').set({"author": "myself" + str(i)}).where(COND("id", "==", i)).apply())
    time.sleep(3)
    print(db.delete_one('books').where(COND("id", "==", i)).apply())
    time.sleep(4)
    i += 1

api.close()
