# CREATE
from space_api import API

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize database(s) you intend to use
db = api.my_sql()

# The book to be created
document = {"name": "SomeAwesomeBook"}

result = db.insert("books").doc(document).apply()
if result.status == 200:
    print("Success")
else:
    print(result.error)


# ----------------------------------------------------------------------------------------------------
# CREATE MULTIPLE
from space_api import API

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize database(s) you intend to use
db = api.my_sql()

# The books to be created
documents = [{"name": "SomeAwesomeBook"},{"name": "AnotherAwesomeBook"}]

result = db.insert("books").docs(documents).apply()
if result.status == 200:
    print("Success")
else:
    print(result.error)
