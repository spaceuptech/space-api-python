from space_api import API

api = API('grpc', 'localhost:8081')
api.set_token('my_secret')

response = api.call('test_service', 'test_func', {'adsf':'adf', 'a':[1,2,3]})
print(response)

api.close()
