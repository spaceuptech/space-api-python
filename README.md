# Python Client API for Space Cloud

## Installation
```bash
$ pip install space-api-py
```

## Documentation
The complete documentation can be found [here](https://spaceuptech.com/docs).

## Quick Start

### Create Client Instance

```python
from space_api import API, AND, OR, COND

api = API('demo-project', 'localhost:8081')

# For MongoDB
db = api.mongo()

# For PostgresQL
db = api.postgres()

# For MySQL
db = api.my_sql()
```
**Note: Multiple databases may be used simultaneously.**

### Insert a document into the database
```python
response = db.insert('books').doc({"name": "MyBook", "author": "John Doe"}).apply()
if response.status == 200:
    # Record successfully inserted
    print("Success")
else:
    # An error occurred
    print(response.error)
```

### Query documents in database
```python
response = db.get('books').sort('-author').apply()
if response.status == 200:
    # We got some result
    print(response.result)
else:
    # An error occurred
    print(response.error)
```

### Update documents in database
```python
response = db.update_one('books').where(COND("author", "==", "some_author")).set({"author": "myself"}).apply()
if response.status == 200:
    # Record successfully updated
    print("Success")
else:
    # An error occurred
    print(response.error)
```

### Delete documents in database
```python
response = db.delete('books').where(COND('name', '!=', 'Book_name')).apply()
if response.status == 200:
    # Record successfully deleted
    print("Success")
else:
    # An error occurred
    print(response.error)
```

### Call functions directly (Function as a Service) 
```python
response = api.call('test_engine', 'test_func', 'params')
print(response)
```

### User Management - Sign In 
```python
response = db.sign_in("user_email", "user_password")
if response.status == 200:
    print(response.result)
else:
    print(response.error)
```

### User Management - Sign Up 
```python
response = db.sign_up("user_email", "user_name", "user_password", "user_role")
if response.status == 200:
    print(response.result)
else:
    print(response.error)
```

### User Management - View Profile 
```python
response = db.profile("user_id")
if response.status == 200:
    print(response.result)
else:
    print(response.error)
```

### User Management - View All Profiles 
```python
response = db.profiles()
if response.status == 200:
    print(response.result)
else:
    print(response.error)
```

### User Management - Edit Profile 
```python
response = db.edit_profile("user_id", email="new_email", name="new_name", password="new_password")
if response.status == 200:
    print(response.result)
else:
    print(response.error)
```

## Authors
[Aliabbas Merchant](https://github.com/AliabbasMerchant) - Initial work

## License

Copyright 2019 Space Up Technologies

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.