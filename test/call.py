from space_api import API

api = API('grpc', 'localhost:8081')
api.set_token('my_secret')

response = api.call('service', 'echo_func', 'param', timeout=5)
print(response)

api.close()
