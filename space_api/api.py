"""
SpaceUp Client Python API
"""
from space_api.sql.sql import SQL
from space_api.mongo.mongo import Mongo


class API:
    """
    The SpaceUp Client API
    ::
        from space_api import API
        api = API("My-Project", "http://localhost:8080")

    :param project_id: (str) The project ID
    :param url: (str) The base URL of space-cloud server
    """

    def __init__(self, project_id: str, url: str):
        self.project_id = project_id
        if url.startswith("http://"):
            self.url = url.lstrip("http://")
        elif url.startswith("https://"):
            self.url = url.lstrip("https://")
        else:
            self.url = url
        print(self.url)
        self.token = None

    def set_token(self, token: str):
        """
        Sets the JWT Token

        :param token: (str) The signed JWT token received from the server on successful authentication
        """
        self.token = token

    def set_project_id(self, project_id: str):
        """
        Sets the Project ID

        :param project_id: (str) The project ID
        """
        self.project_id = project_id

    def mongo(self) -> 'Mongo':
        """
        Returns a MongoDB client instance

        :return: MongoDB client instance
        """
        return Mongo(self.project_id, self.url, self.token)

    def postgres(self) -> 'SQL':
        """
        Returns a Postgres client instance

        :return: Postgres client instance
        """
        return SQL(self.project_id, self.url, 'sql-postgres', self.token)

    def my_sql(self) -> 'SQL':
        """
        Returns a MySQL client instance

        :return: MySQL client instance
        """
        return SQL(self.project_id, self.url, 'sql-mysql', self.token)

    def __str__(self):
        return f'SpaceAPI(project_id:{self.project_id}, url:{self.url}, token:{self.token})'

    def call(self, engine_name: str, func_name: str, params, timeout: int = 5000):
        raise NotImplementedError("Coming Soon!")

    def file_store(self):
        raise NotImplementedError("Coming Soon!")
