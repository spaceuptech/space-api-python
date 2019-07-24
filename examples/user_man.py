# User Management
from space_api import API

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize database(s) you intend to use
db = api.my_sql()

# Sign Up
response = db.sign_up("user_email", "user_name", "user_password", "user_role")
if response.status == 200:
    print(response.result)
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# Sign In
response = db.sign_in("user_email", "user_password")
if response.status == 200:
    print(response.result)
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# View Profile
response = db.profile("user_id")
if response.status == 200:
    print(response.result)
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# View All Profiles
response = db.profiles()
if response.status == 200:
    print(response.result)
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# Edit Profile
response = db.edit_profile("user_id", email="new_email", name="new_name", password="new_password")
if response.status == 200:
    print(response.result)
else:
    print(response.error)
