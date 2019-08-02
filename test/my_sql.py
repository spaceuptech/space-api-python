from space_api import API, COND

api = API('books-app', 'localhost:4124')
db = api.my_sql()

# testing
print(db.delete('books').apply())

# insert
print("all")
print(db.insert('books').docs([{"name": "BookName"}, {"name": "BookName"}]).apply())
print("one")
print(db.insert('books').doc({"name": "MyBook", "author": "John Doe"}).apply())


# get
print("all")
print(db.get('books').apply())
print("one")
print(db.get_one('books').apply())
print("limit all")
print(db.get('books').limit(2).apply())
print("limit one")
print(db.get_one('books').limit(2).apply())
print("skip all")
print(db.get('books').skip(2).apply())
print("skip one")
print(db.get_one('books').skip(2).apply())
print("sort all")
print(db.get('books').sort('-author').apply())
print("sort one")
print(db.get_one('books').sort('author').apply())
print("select all")
print(db.get('books').select({'author': 1}).apply())
print("select one")
print(db.get_one('books').select({'author': 1}).apply())
print("where all")
print(db.get('books').where(COND("name", "==", "Book_name")).apply())
print("where one")
print(db.get_one('books').where(COND("name", "==", "BookName")).apply())
print("distinct")
print(db.distinct("books").key("author").apply())
print("count")
print(db.count("books").apply())
print("count where")
print(db.count("books").where(COND("author", "==", "Jon Doe")).apply())


# update
print("set")
print(db.update('books').set({"author": "myself"}).apply())
print("set where")
print(db.update('books').where(COND("author", "==", "some_author")).set({"author": "myself"}).apply())
print("upsert")
print(db.upsert('books').set({"author": "myself"}).where(COND("id", "==", 1211)).apply())
print("upsert where")
print(db.upsert('books').where(COND("author", "==", "some_author")).set({"author": "myself"}).apply())
print("update inc")
print(db.update("books").inc({'views': 10}).apply())
print("update mul")
print(db.update("books").mul({'views': 10}).apply())
print("update max")
print(db.update("books").max({'views': 10000}).apply())
print("update min")
print(db.update("books").min({'views': 10}).apply())
print("update current_date")
print(db.update("books").current_date('views').apply())
print("upsert current_date where")
print(db.upsert('books').current_date("views").where(COND("id", "==", 122)).apply())


# testing
print(db.get('books').apply())


# deletee
print("all")
print(db.delete('books').apply())
print("one")
print(db.delete_one('books').apply())
print("where, all")
print(db.delete('books').where(COND('name', '!=', 'Book_name')).apply())
print("where, one")
print(db.delete_one('books').where(COND('name', '!=', 'Book_name')).apply())


# testing
print(db.get('books').apply())

api.close()
