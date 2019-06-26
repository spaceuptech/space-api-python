from space_api import API
import time
import threading
import random

api = API('books-app', '192.168.43.226:8081')
db = api.mongo()


def on_snapshot(docs, kind):
    print(docs)


def on_error(error):
    print("ERROR:", error)


while True:
    unsubscribe = db.live_query('books').subscribe(on_snapshot, on_error)
    time.sleep(random.randint(1, 5))
    unsubscribe()
    print("Closed")


# def do_not_die():
#     while True:
#         time.sleep(0.01)
#
#
# thread = threading.Thread(target=do_not_die)
# thread.start()
# thread.join()

api.close()
