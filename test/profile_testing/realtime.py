from space_api import API
import time
import random
import variables

api = API(variables.app, variables.url)
db = variables.db(api)


def on_snapshot(docs, kind):
    print(docs)


def on_error(error):
    print("ERROR:", error)


while True:
    unsubscribe = db.live_query('books').subscribe(on_snapshot, on_error)
    time.sleep(random.randint(1, 5))
    unsubscribe()
    print("Closed")

api.close()
