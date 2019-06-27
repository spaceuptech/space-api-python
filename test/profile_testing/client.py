from space_api import API
import random
import time
import variables

api = API(variables.app, variables.url)

while True:
    response = api.call('service', 'echo_func', 'param' + str(random.randint(1,100)), timeout=5)
    print(response)
    time.sleep(0.01)

api.close()
