# READ
from space_api import API, AND, OR, COND

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize database(s) you intend to use
db = api.my_sql()

# The condition to be matched
condition = COND("id", "==", "1")

# Get the books
response = db.get("books").where(condition).apply()
if response.status == 200:
    print(response.result)
else:
    print(response.error)

# ----------------------------------------------------------------------------------------------------
# READ ONE
from space_api import API, AND, OR, COND

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize database(s) you intend to use
db = api.my_sql()

# The condition to be matched
condition = COND("author", "==", "SomeAuthor")

# Get the book
response = db.get_one("books").where(condition).apply()
if response.status == 200:
    print(response.result)
else:
    print(response.error)

# ----------------------------------------------------------------------------------------------------
# READ MULTIPLE CONDITIONS
from space_api import API, AND, OR, COND

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize database(s) you intend to use
db = api.my_sql()

# The condition to be matched
condition = AND(COND("id", "==", "1"), COND("author", "==", "SomeAuthor"))

# Get the books
response = db.get("books").where(condition).apply()
if response.status == 200:
    print(response.result)
else:
    print(response.error)

# ----------------------------------------------------------------------------------------------------
# READ SELECT
from space_api import API, AND, OR, COND

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize database(s) you intend to use
db = api.my_sql()

# The condition to be matched
condition = COND("author", "==", "SomeAuthor")

# Get the books
response = db.get("books").where(condition).select({"name": 1}).apply()
if response.status == 200:
    print(response.result)
else:
    print(response.error)

# ----------------------------------------------------------------------------------------------------
# READ SORT
from space_api import API, AND, OR, COND

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize database(s) you intend to use
db = api.my_sql()

# The condition to be matched
condition = COND("author", "==", "SomeAuthor")

# Get the books
response = db.get("books").where(condition).sort("name", "-id").apply()
# "name" -> sort by name, ascending order
# "-name" -> sort by name, descending order
if response.status == 200:
    print(response.result)
else:
    print(response.error)

# ----------------------------------------------------------------------------------------------------
# READ SKIP
from space_api import API, AND, OR, COND

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize database(s) you intend to use
db = api.my_sql()

# The condition to be matched
condition = COND("author", "==", "SomeAuthor")

# Get the books
response = db.get("books").where(condition).skip(1).apply()
if response.status == 200:
    print(response.result)
else:
    print(response.error)

# ----------------------------------------------------------------------------------------------------
# READ LIMIT
from space_api import API, AND, OR, COND

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize database(s) you intend to use
db = api.my_sql()

# The condition to be matched
condition = COND("author", "==", "SomeAuthor")

# Get the books
response = db.get("books").where(condition).limit(2).apply()
if response.status == 200:
    print(response.result)
else:
    print(response.error)

# ----------------------------------------------------------------------------------------------------
# READ DISTINCT
from space_api import API, COND

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize database(s) you intend to use
db = api.mongo()

# The condition to be matched
condition = COND("author", "==", "SomeAuthor")

# Get the books
response = db.distinct("books").where(condition).apply()
if response.status == 200:
    print(response.result)
else:
    print(response.error)

# ----------------------------------------------------------------------------------------------------
# READ COUNT
from space_api import API, COND

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize database(s) you intend to use
db = api.mongo()

# The condition to be matched
condition = COND("author", "==", "SomeAuthor")

# Get the books
response = db.count("books").where(condition).apply()
if response.status == 200:
    print(response.result)
else:
    print(response.error)

# ----------------------------------------------------------------------------------------------------
# READ AGGREGATE
from space_api import API, COND

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize database(s) you intend to use
db = api.mongo()

pipe = [
    {"$match": {"status": "A"}},
    {"$group": {"_id": "$cust_id", "total": {"$sum": "amount"}}}
]

# Get the books
response = db.aggr("books").pipe(pipe).apply()
if response.status == 200:
    print(response.result)
else:
    print(response.error)
