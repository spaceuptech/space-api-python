from space_api import API

api = API('books-app', 'localhost:4124')


def my_func(params, auth, cb):  # Function to be registered
    print("Params", params, "Auth", auth)

    # Do Something
    cb('response', {"ack": True})


service = api.service('service')  # Create an instance of service
service.register_func('my_func', my_func)  # Register function
service.start()  # Start service

# Call function of some other service
response = api.call('some_service', 'some_func', {"msg": "space-service-go is awesome!"}, timeout=5)
print(response)

api.close()
