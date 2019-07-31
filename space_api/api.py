"""
SpaceUp Client Python API
"""
from typing import Optional
from space_api.db.db import DB
from space_api.response import Response
from space_api.service import Service
from space_api.filestore import FileStore
from space_api.transport import Transport
from space_api import constants


class API:
    """
    The SpaceUp Client API
    ::
        from space_api import API
        api = API("My-Project", "localhost:4124")

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
        self.transport = Transport(self.url, self.project_id)

    def close(self):
        """
        Closes the communication channel
        """
        self.transport.close()

    def connect(self):
        """
        Connects to the Space Cloud Instance
        """
        self.transport.connect()

    def set_token(self, token: str):
        """
        Sets the JWT Token

        :param token: (str) The signed JWT token received from the server on successful authentication
        """
        self.token = token
        self.transport.token = token

    def set_project_id(self, project_id: str):
        """
        Sets the Project ID

        :param project_id: (str) The project ID
        """
        self.project_id = project_id
        self.transport.project_id = project_id

    def mongo(self) -> 'DB':
        """
        Returns a MongoDB client instance

        :return: MongoDB client instance
        """
        return DB(self.transport, constants.Mongo)

    def postgres(self) -> 'DB':
        """
        Returns a Postgres client instance

        :return: Postgres client instance
        """
        return DB(self.transport, constants.Postgres)

    def my_sql(self) -> 'DB':
        """
        Returns a MySQL client instance

        :return: MySQL client instance
        """
        return DB(self.transport, constants.MySQL)

    def __str__(self) -> str:
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
        return self.transport.faas(service_name, func_name, params, timeout)

    def service(self, service: str) -> 'Service':
        """
        Returns a Service instance

        :param service: (str) The name of the service
        :return: (Service) The Service instance
        """
        return Service(self.transport, service)

    def file_store(self) -> 'FileStore':
        """
        Returns a FileStore instance

        :return: (FileStore) The Service instance
        """
        return FileStore(self.transport)


__all__ = ["API"]
