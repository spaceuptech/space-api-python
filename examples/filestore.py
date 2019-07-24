# LIST FILES
from space_api import API

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize file storage module
file_store = api.file_store()

# List all the files in a particular location ("\\" [remote])
response = file_store.list_files("\\")
if response.status == 200:
    print(response.result)
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# CREATE FOLDER

from space_api import API

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize file storage module
file_store = api.file_store()

# Create a folder ("folder" [remote]) in the location ("\\" [remote])
response = file_store.create_folder("\\", "folder")
if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# DELETE A FILE
from space_api import API

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize file storage module
file_store = api.file_store()

# Delete a file ("\\a.txt" [remote])
response = file_store.delete_file("\\a.txt")
if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# UPLOAD A FILE
from space_api import API

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize file storage module
file_store = api.file_store()

# Upload a file (to be named "new.txt" [remote]) into location ("\\" [remote]) from a file ("a.txt" [local])
response = file_store.upload_file("\\", "new.txt", "a.txt")
if response.status == 200:
    print("Success")
else:
    print(response.error)


# ----------------------------------------------------------------------------------------------------
# DOWNLOAD A FILE

from space_api import API

# Initialize api with the project name and url of the space cloud
api = API("books-app", "localhost:4124")

# Initialize file storage module
file_store = api.file_store()

# Download the file ("\\a.txt" [remote]) into a file ("b.txt" [local])
response = file_store.download_file("\\a.txt", "b.txt")
if response.status == 200:
    print("Success")
else:
    print(response.error)


