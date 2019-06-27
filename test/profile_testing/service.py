from space_api import API
import variables

api = API(variables.app, variables.url)

service = api.service(variables.service)


def echo_func(params, auth, cb):
    cb('response', params)


# def func2(params, auth, cb):
#     cb('response', 'my_response')


service.register_func('echo_func', echo_func)
# service.register_func('func2', func2)

service.start()
api.close()
