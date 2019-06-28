from space_api import API

api = API('books-app', 'localhost:8081')

for i in range(100):
    response = api.call('service', 'echo_func', 'param' + str(i), timeout=5)
    print(response)

api.close()
