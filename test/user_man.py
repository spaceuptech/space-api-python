from space_api import API

api = API('books-app', 'localhost:4124')

db = api.my_sql()

response = db.sign_up("user_email", "user_name", "user_password", "user_role")
print(response)

response = db.sign_in("user_email", "user_password")
_id = response.result["user"]["id"]
print(response)

response = db.profile(_id)
print(response)

response = db.profiles()
print(response)

response = db.edit_profile(_id, email="new_email", name="new_name", password="new_password")
print(response)

response = db.edit_profile(_id, email="newer_email", name="newer_name")
print(response)

response = db.edit_profile(_id, email="newest_email", password="newest_password")
print(response)

response = db.edit_profile(_id, password="even_newer_password")
print(response)

response = db.edit_profile(_id, name="even_newer_name")
print(response)

api.close()
