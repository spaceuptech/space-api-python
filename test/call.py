from space_api import API

api = API('books-app', 'localhost:4124')

for i in range(100):
    response = api.call('service', 'echo_func', 'param' + str(i), timeout=5000)
    print(response)

api.close()
