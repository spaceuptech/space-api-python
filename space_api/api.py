from space_api.sql.sql import SQL
from space_api.mongo.mongo import Mongo


class API:
    def __init__(self, project_id, url):
        self.project_id = project_id
        self.url = url
        self.token = None

    def set_token(self, token: str):
        self.token = token

    def set_project_id(self, project_id: str):
        self.project_id = project_id

    def mongo(self):
        return Mongo(self.project_id, self.url, self.token)

    def postgres(self):
        return SQL(self.project_id, self.url, 'sql-postgres', self.token)

    def my_sql(self):
        return SQL(self.project_id, self.url, 'sql-mysql', self.token)

    def call(self, engine_name: str, func_name: str, params, timeout: int = 5000):
        raise NotImplementedError("Coming Soon!")

    def file_store(self):
        raise NotImplementedError("Coming Soon!")
