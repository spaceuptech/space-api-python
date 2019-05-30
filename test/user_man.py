from space_api import API

api = API('grpc', 'localhost:8081')
api.set_token('my_secret')

db = api.my_sql()
response = db.sign_up("user_email1", "user_name", "user_password", "user_role")
print(response)

response = db.sign_in("user_email", "user_password")
_id = response.result["user"]["id"]
print(response)

response = db.profile(_id)
print(response)

response = db.profiles()
print(response)

response = db.edit_profile(_id, "user_password", "new_email", "new_name", "new_password")
print(response)

response = db.edit_profile(_id, "user_password", "new_email", "new_name")
print(response)

response = db.edit_profile(_id, "user_password", "new_email", "new_password")
print(response)

api.close()
