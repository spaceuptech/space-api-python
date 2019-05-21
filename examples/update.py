# UPDATE
from space_api import API, AND, OR, COND
api = API("books-app", "localhost:8081")
db = api.my_sql()

# The condition to be matched
condition = COND("author", "==", "author1")

# Update the books
response = db.update("books").where(condition).set({"name": "A book"}).apply()

if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# UPDATE ONE
from space_api import API, AND, OR, COND
api = API("books-app", "localhost:8081")
db = api.my_sql()

# The condition to be matched
condition = COND("author", "==", "author1")

# Update the books
response = db.update_one("books").where(condition).set({"name": "A book"}).apply()

if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# UPDATE CONDITION
from space_api import API, AND, OR, COND
api = API("books-app", "localhost:8081")
db = api.my_sql()

# The condition to be matched
condition = COND("author", "==", "author1")

# Update the books
response = db.update("books").where(condition).set({"name": "A book"}).apply()

if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# UPDATE MULTIPLE CONDITIONS
from space_api import API, AND, OR, COND
api = API("books-app", "localhost:8081")
db = api.my_sql()

# The condition to be matched
condition = AND(COND("author", "==", "author1"), COND("name", "==", "someBook"))

# Update the books
response = db.update("books").where(condition).set({"name": "A book"}).apply()

if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# UPDATE SET
from space_api import API, AND, OR, COND
api = API("books-app", "localhost:8081")
db = api.my_sql()

# The condition to be matched
condition = COND("author", "==", "author1")

# Update the books
response = db.update("books").where(condition).set({"name": "A book"}).apply()

if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# UPDATE UPSERT
from space_api import API, COND
api = API("books-app", "localhost:8081")
db = api.mongo()

# The condition to be matched
condition = COND("author", "==", "author1")

# Update the books
response = db.upsert("books").where(condition).set({"name": "A book"}).apply()

if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# UPDATE PUSH
from space_api import API, COND
api = API("books-app", "localhost:8081")
db = api.mongo()

# The condition to be matched
condition = COND("author", "==", "author1")

# Update the books
response = db.update("books").where(condition).push({"name": "A book"}).apply()

if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# UPDATE REMOVE
from space_api import API, COND
api = API("books-app", "localhost:8081")
db = api.mongo()

# The condition to be matched
condition = COND("author", "==", "author1")

# Update the books
response = db.update("books").where(condition).remove("author").apply()

if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# UPDATE RENAME
from space_api import API, COND
api = API("books-app", "localhost:8081")
db = api.mongo()

# The condition to be matched
condition = COND("author", "==", "author1")

# Update the books
response = db.update("books").where(condition).rename({"writer":"author"}).apply()

if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# UPDATE INC
from space_api import API, COND
api = API("books-app", "localhost:8081")
db = api.mongo()

# The condition to be matched
condition = COND("author", "==", "author1")

# Update the books
response = db.update("books").where(condition).inc({"likes":1}).apply()

if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# UPDATE MUL
from space_api import API, COND
api = API("books-app", "localhost:8081")
db = api.mongo()

# The condition to be matched
condition = COND("author", "==", "author1")

# Update the books
response = db.update("books").where(condition).mul({"likes":10}).apply()

if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# UPDATE MAX
from space_api import API, COND
api = API("books-app", "localhost:8081")
db = api.mongo()

# The condition to be matched
condition = COND("author", "==", "author1")

# Update the books
response = db.update("books").where(condition).max({"likes":100}).apply()

if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# UPDATE MIN
from space_api import API, COND
api = API("books-app", "localhost:8081")
db = api.mongo()

# The condition to be matched
condition = COND("author", "==", "author1")

# Update the books
response = db.update("books").where(condition).min({"likes":100}).apply()

if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# UPDATE CURRENT TIMESTAMP
from space_api import API, COND
api = API("books-app", "localhost:8081")
db = api.mongo()

# The condition to be matched
condition = COND("author", "==", "author1")

# Update the books
response = db.update("books").where(condition).current_timestamp("last_read").apply()

if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# UPDATE CURRENT DATE
from space_api import API, COND
api = API("books-app", "localhost:8081")
db = api.mongo()

# The condition to be matched
condition = COND("author", "==", "author1")

# Update the books
response = db.update("books").where(condition).current_date("last_read").apply()

if response.status == 200:
    print("Success")
else:
    print(response.error)
