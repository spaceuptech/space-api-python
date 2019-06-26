import time
import random
from space_api import API, COND

api = API('books-app', '192.168.43.226:8081')
db = api.mongo()
db.delete('books').apply()

start = time.time()


def func(op_sel, i):
    if op_sel == 0:
        db.insert('books').doc({"_id": i, "name": "MyBook" + str(i), "author": "Author" + str(i)}).apply()
    elif op_sel == 1:
        db.update('books').set({"author": "myself" + str(i)}).where(COND("_id", "==", i)).apply()
    elif op_sel == 2:
        db.delete_one('books').where(COND("_id", "==", i)).apply()
    else:
        db.get('books').apply()


while True:
    sel = random.randint(0, 3)
    id = random.randint(0, 9)
    func(sel, id)
    s = time.time()
    # print()
    a = s - start
    print(a)
    # for i in range(int(a*100)):
    #     print("X", end="")
    # print()
    start = s

    # time.sleep(0.01)
