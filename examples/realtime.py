from space_api import API

api = API('books-app', 'localhost:8081')
db = api.my_sql()


def on_snapshot(docs, kind):
    print("DOCS:", docs)
    print("KIND OF LIVE QUERY:", kind)


def on_error(error):
    print("ERROR:", error)


unsubscribe = db.live_query('books').subscribe(on_snapshot, on_error)

# After some logic/condition
unsubscribe()
api.close()
