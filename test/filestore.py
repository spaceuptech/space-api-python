from space_api import API

api = API('books-app', 'localhost:4124')

file_store = api.file_store()

print(file_store.list_files("\\"))

print(file_store.create_folder("\\", "folder2"))

print(file_store.list_files("\\"))

print(file_store.delete_file("\\folder2"))

print(file_store.list_files("\\"))

print(file_store.upload_file("\\Folder\\Folder", "b.txt", "a.txt"))

print(file_store.download_file("\\Folder\\Folder\\b.txt", "b.txt"))
