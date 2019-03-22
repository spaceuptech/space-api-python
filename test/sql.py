from space_api import API

api = API('test', 'http://localhost:8080')
db = api.my_sql()
doc = {"_id": 1, "title": "Title 1", "content": "My first record"}
result = db.insert('collection').one(doc)
print(result)
