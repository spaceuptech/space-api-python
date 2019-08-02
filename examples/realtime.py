import time
from space_api import API

api = API('books-app', 'localhost:4124')
db = api.my_sql()


def on_snapshot(docs, kind, changed):
    print("DOCS:", docs)
    print("KIND OF LIVE QUERY:", kind)
    print("CHANGED DOC:", changed)
    print()


def on_error(error):
    print("ERROR:", error)


subscription = db.live_query('books').subscribe(on_snapshot, on_error)
time.sleep(1)
print(subscription.get_snapshot())

# After some logic/condition
subscription.unsubscribe()
api.close()
