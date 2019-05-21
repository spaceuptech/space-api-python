# DELETE
from space_api import API, COND

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:8081")

# Initialize database(s) you intend to use
db = api.my_sql()

# The condition to be matched
condition = COND("name", "==", "SomeAwesomeBook")

# Delete all books which match a particular condition
response = db.delete("books").where(condition).apply()
if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# DELETE ONE
from space_api import API, COND

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:8081")

# Initialize database(s) you intend to use
db = api.my_sql()

# The condition to be matched
condition = COND("name", "==", "SomeAwesomeBook")

# Delete all books which match a particular condition
response = db.delete_one("books").where(condition).apply()
if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# DELETE MULTIPLE CONDITIONS
from space_api import API, COND, OR, AND

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:8081")

# Initialize database(s) you intend to use
db = api.my_sql()

# The condition to be matched
condition = AND(COND("name", "==", "SomeAwesomeBook"), COND("author", "==", "SomeAuthor"))

# Delete all books which match a particular condition
response = db.delete("books").where(condition).apply()
if response.status == 200:
    print("Success")
else:
    print(response.error)

