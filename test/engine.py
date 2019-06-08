from space_api import API

api = API('grpc', 'localhost:8081')
api.set_token('my_secret')

service = api.service('service')


def echo_func(params, auth):
    return params + params


def func2(params, auth):
    return 'my_response'


service.register_function(echo_func)
service.register_function(func2)

service.start()
api.close()
