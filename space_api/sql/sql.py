from typing import Optional
from space_api.sql.get import Get
from space_api.sql.insert import Insert
from space_api.sql.update import Update
from space_api.sql.delete import Delete


class SQL:
    def __init__(self, project_id: str, url: str, db_type: str, token: Optional[str] = None):
        self.project_id = project_id
        self.url = url
        self.db_type = db_type
        self.token = token

    def get(self, collection: str):
        return Get(self.project_id, collection, self.url, self.db_type, self.token)

    def insert(self, collection: str):
        return Insert(self.project_id, collection, self.url, self.db_type, self.token)

    def update(self, collection: str):
        return Update(self.project_id, collection, self.url, self.db_type, self.token)

    def delete(self, collection: str):
        return Delete(self.project_id, collection, self.url, self.db_type, self.token)

    def live_query(self, collection: str):
        raise NotImplementedError("Coming Soon!")

    def profile(self, id: str):
        raise NotImplementedError("Coming Soon!")

    def edit_profile(self, id: str, email: str, name: str, password: str):
        raise NotImplementedError("Coming Soon!")

    def profiles(self):
        raise NotImplementedError("Coming Soon!")

    def sign_in(self, email: str, password: str):
        raise NotImplementedError("Coming Soon!")

    def sign_up(self, email: str, name: str, password: str, role: str):
        raise NotImplementedError("Coming Soon!")


__all__ = ['SQL']
