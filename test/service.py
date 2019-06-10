from space_api import API

api = API('grpc', 'localhost:8081')
api.set_token('my_secret')

service = api.service('service')


def echo_func(params, auth, cb):
    cb('response', params)


def func2(params, auth, cb):
    cb('response', 'my_response')


service.register_function('echo_func', echo_func)
service.register_function('func2', func2)

service.start()
api.close()
