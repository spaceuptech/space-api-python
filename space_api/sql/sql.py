from typing import Optional
from space_api.sql.get import Get
from space_api.sql.insert import Insert
from space_api.sql.update import Update
from space_api.sql.delete import Delete


class SQL:
    """
    The SQL Client Interface
    ::
        from space_api import API
        api = API("My-Project", "http://localhost:8080")
        db = api.my_sql() # For a MySQL interface
        db = api.postgres() # For a Postgres interface

    :param project_id: (str) The project ID
    :param url: (str) The project URL
    :param db_type: (str) The database type
    :param token: (str) The (optional) JWT Token
    """

    def __init__(self, project_id: str, url: str, db_type: str, token: Optional[str] = None):
        self.project_id = project_id
        self.url = url
        self.db_type = db_type
        self.token = token

    def __str__(self):
        if self.db_type == 'sql-mysql':
            return f'SpaceAPI MySQL(project_id:{self.project_id}, url:{self.url}, token:{self.token})'
        elif self.db_type == 'sql-postgres':
            return f'SpaceAPI Postgres(project_id:{self.project_id}, url:{self.url}, token:{self.token})'

    def get(self, collection: str) -> 'Get':
        """
        Returns an SQL Get object
        
        :param collection: (str) The collection name
        :return: The SQL Get object
        """
        return Get(self.project_id, collection, self.url, self.db_type, self.token)

    def insert(self, collection: str) -> 'Insert':
        """
        Returns an SQL Insert object

        :param collection: (str) The collection name
        :return: The SQL Insert object
        """
        return Insert(self.project_id, collection, self.url, self.db_type, self.token)

    def update(self, collection: str) -> 'Update':
        """
        Returns an SQL Update object

        :param collection: (str) The collection name
        :return: The SQL Update object
        """
        return Update(self.project_id, collection, self.url, self.db_type, self.token)

    def delete(self, collection: str) -> 'Delete':
        """
        Returns an SQL Delete object

        :param collection: (str) The collection name
        :return: The SQL Delete object
        """
        return Delete(self.project_id, collection, self.url, self.db_type, self.token)

    def live_query(self, collection: str):
        raise NotImplementedError("Coming Soon!")

    def profile(self, _id: str):
        raise NotImplementedError("Coming Soon!")

    def edit_profile(self, _id: str, email: str, name: str, password: str):
        raise NotImplementedError("Coming Soon!")

    def profiles(self):
        raise NotImplementedError("Coming Soon!")

    def sign_in(self, email: str, password: str):
        raise NotImplementedError("Coming Soon!")

    def sign_up(self, email: str, name: str, password: str, role: str):
        raise NotImplementedError("Coming Soon!")


__all__ = ['SQL']
