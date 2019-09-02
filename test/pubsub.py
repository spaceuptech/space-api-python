import time
import threading
from space_api import API

api = API('books-app', 'localhost:4124')
pubsub = api.pubsub()


def on_receive(subject, msg):
    print("received", subject, msg)


subscription = pubsub.subscribe("/subject/", on_receive)
print(subscription)


def publish():
    for i in range(30):
        msg = [1, "adf", 5.2, True, {"k": "v"}, [1, "b"]]
        print("publishing", msg, pubsub.publish("/subject/a/", msg))
        time.sleep(2)


thread = threading.Thread(target=publish)
thread.start()
thread.join()

subscription.unsubscribe()
api.close()
