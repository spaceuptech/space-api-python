import time
import random
from space_api import API, COND
import variables

api = API(variables.app, variables.url)
db = variables.db(api)
db.delete('books').apply()


def func(op_sel, i):
    if op_sel == 0:
        return db.insert('books').doc({variables.id: i, "name": "MyBook" + str(i), "author": "Author" + str(i)}).apply()
    elif op_sel == 1:
        return db.update('books').set({"author": "myself" + str(i)}).where(COND(variables.id, "==", i)).apply()
    elif op_sel == 2:
        return db.delete_one('books').where(COND(variables.id, "==", i)).apply()
    else:
        return db.get('books').apply()


while True:
    sel = random.randint(0, 3)
    id = random.randint(0, 9)
    start = time.time()
    print(func(sel, id).error)
    s = time.time()
    print(s - start)
    # for i in range(int(a*100)):
    #     print("X", end="")
    # print()

    # time.sleep(0.01)
