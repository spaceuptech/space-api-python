from space_api import API
import time
import threading

api = API('books-app', 'localhost:8081')
db = api.my_sql()


def on_snapshot(docs, type):
    print("DOCS:", docs)
    print("TYPE:", type)


def on_error(error):
    print("ERROR:", error)


unsubscribe = db.live_query('books').options(changes_only=False).subscribe(on_snapshot, on_error)


def do_not_die():
    for i in range(24):
        # print("Sleeping...")
        time.sleep(1)


thread = threading.Thread(target=do_not_die)
thread.start()
thread.join()

unsubscribe()
api.close()
