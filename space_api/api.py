"""
SpaceUp Client Python API
"""
import grpc
from typing import Optional
from space_api.proto.server_pb2_grpc import SpaceCloudStub
from space_api.sql.sql import SQL
from space_api.mongo.mongo import Mongo
from space_api.transport import faas
from space_api.response import Response


class API:
    """
    The SpaceUp Client API
    ::
        from space_api import API
        api = API("My-Project", "localhost:8080")

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
        self.token = None
        self.channel = grpc.insecure_channel(self.url)
        self.stub = SpaceCloudStub(self.channel)

    def close(self):
        self.channel.close()

    def connect(self):
        self.channel = grpc.insecure_channel(self.url)
        self.stub = SpaceCloudStub(self.channel)

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
        return Mongo(self.project_id, self.stub, self.token)

    def postgres(self) -> 'SQL':
        """
        Returns a Postgres client instance

        :return: Postgres client instance
        """
        return SQL(self.project_id, self.stub, 'sql-postgres', self.token)

    def my_sql(self) -> 'SQL':
        """
        Returns a MySQL client instance

        :return: MySQL client instance
        """
        return SQL(self.project_id, self.stub, 'sql-mysql', self.token)

    def __str__(self):
        return f'SpaceAPI(project_id:{self.project_id}, url:{self.url}, token:{self.token})'

    def call(self, service_name: str, func_name: str, params, timeout: Optional[int] = 5000) -> Response:
        """
        Calls a function from Function as a Service Engine
        ::
            response = api.call('my-service', 'my-func', { msg: 'Function as a Service is awesome!' }, 1000)
        
        :param service_name: (str) The name of service(engine) with which the function is registered
        :param func_name: (str) The name of function to be called
        :param params: The params for the function
        :param timeout: (int) The (optional) timeout in milliseconds (defaults to 5000)
        :return: (Response) The response object containing values corresponding to the request
        """
        return faas(self.stub, params, timeout, service_name, func_name, self.token)

    def file_store(self):
        raise NotImplementedError("Coming Soon!")


__all__ = ["API"]
