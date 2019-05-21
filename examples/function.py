from space_api import API

api = API("books-app", "localhost:8081")
# Call a function, 'my-func' of 'my-engine' running on backend
response = api.call('my-engine', 'my-func', {"msg": 'Space Cloud is awesome!'}, 1000)
if response.status == 200:
    print(response.result)
else:
    print(response.error)
