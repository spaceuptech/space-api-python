from typing import Optional
from space_api.sql.get import Get
from space_api.sql.insert import Insert
from space_api.sql.update import Update
from space_api.sql.delete import Delete
from space_api.sql.batch import Batch
from space_api.response import Response
from space_api.proto.server_pb2_grpc import SpaceCloudStub
from space_api import user_man


class SQL:
    """
    The SQL Client Interface
    ::
        from space_api import API
        api = API("My-Project", "localhost:8080")
        db = api.my_sql() # For a MySQL interface
        db = api.postgres() # For a Postgres interface

    :param project_id: (str) The project ID
    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param db_type: (str) The database type
    :param token: (str) The (optional) JWT Token
    """

    def __init__(self, project_id: str, stub: SpaceCloudStub, db_type: str, token: Optional[str] = None):
        self.project_id = project_id
        self.stub = stub
        self.db_type = db_type
        self.token = token

    def __str__(self) -> str:
        if self.db_type == 'sql-mysql':
            return f'SpaceAPI MySQL(project_id:{self.project_id}, stub:{self.stub}, token:{self.token})'
        elif self.db_type == 'sql-postgres':
            return f'SpaceAPI Postgres(project_id:{self.project_id}, stub:{self.stub}, token:{self.token})'

    def get(self, collection: str) -> 'Get':
        """
        Returns an SQL Get object, with operation 'all'
        
        :param collection: (str) The collection name
        :return: The SQL Get object
        """
        return Get(self.project_id, collection, self.stub, self.db_type, self.token)

    def get_one(self, collection: str) -> 'Get':
        """
        Returns an SQL Get object, with operation 'one'

        :param collection: (str) The collection name
        :return: The SQL Get object
        """
        return Get(self.project_id, collection, self.stub, self.db_type, self.token, operation='one')

    def insert(self, collection: str) -> 'Insert':
        """
        Returns an SQL Insert object

        :param collection: (str) The collection name
        :return: The SQL Insert object
        """
        return Insert(self.project_id, collection, self.stub, self.db_type, self.token)

    def update(self, collection: str) -> 'Update':
        """
        Returns an SQL Update object, with operation 'all'

        :param collection: (str) The collection name
        :return: The SQL Update object
        """
        return Update(self.project_id, collection, self.stub, self.db_type, self.token)

    def update_one(self, collection: str) -> 'Update':
        """
        Returns an SQL Update object, with operation 'one'

        :param collection: (str) The collection name
        :return: The SQL Update object
        """
        return Update(self.project_id, collection, self.stub, self.db_type, self.token, operation='one')

    def delete(self, collection: str) -> 'Delete':
        """
        Returns an SQL Delete object, with operation 'all'

        :param collection: (str) The collection name
        :return: The SQL Delete object
        """
        return Delete(self.project_id, collection, self.stub, self.db_type, self.token)

    def delete_one(self, collection: str) -> 'Delete':
        """
        Returns an SQL Delete object, with operation 'one'

        :param collection: (str) The collection name
        :return: The SQL Delete object
        """
        return Delete(self.project_id, collection, self.stub, self.db_type, self.token, operation='one')

    def begin_batch(self) -> 'Batch':
        """
        Creates a Batch request
        ::
            batch_obj = db.begin_batch()
            batch_obj.add(...)
            response = batch_obj.apply()

        :return: (Batch) A SQL Batch object
        """
        return Batch(self.project_id, self.stub, self.db_type, self.token)

    def live_query(self, collection: str):
        raise NotImplementedError("Coming Soon!")

    def profile(self, _id: str) -> Response:
        """
        Gets the profile of the user
        ::
            response = db.profile("user_id")

        :param _id: (str) The user's id
        :return: (Response) The response object containing values corresponding to the request
        """
        return user_man.profile(self.project_id, self.db_type, self.token, self.stub, _id)

    def profiles(self) -> Response:
        """
        Gets the all the profiles
        ::
            response = db.profile()

        :return: (Response) The response object containing values corresponding to the request
        """
        return user_man.profiles(self.project_id, self.db_type, self.token, self.stub)

    def edit_profile(self, _id: str, email: Optional[str] = None, name: Optional[str] = None,
                     password: Optional[str] = None) -> Response:
        """
        Edits the profile of the user
        ::
            response = db.edit_profile("user_id", "new_email", "new_name", "new_password")

        :param _id: (str) The user's id
        :param email: (str) The (optional) new email id
        :param name: (str) Then (optional) new name
        :param password: (str) The (optional) new password
        :return: (Response) The response object containing values corresponding to the request
        """
        return user_man.edit_profile(self.project_id, self.db_type, self.token, self.stub, _id, email, name, password)

    def sign_in(self, email: str, password: str) -> Response:
        """
        Allows the user to sign in
        ::
            response = db.sign_in("user_email", "user_password")

        :param email: (str) The user's email id
        :param password: (str) The user's password
        :return: (Response) The response object containing values corresponding to the request
        """
        return user_man.sign_in(self.project_id, self.db_type, self.token, self.stub, email, password)

    def sign_up(self, email: str, name: str, password: str, role: str) -> Response:
        """
        Allows a user to sign up
        ::
            response = db.sign_up("user_email", "user_name", "user_password", "user_role")

        :param email: (str) The user's email id
        :param name: (str) The user's name
        :param password: (str) The user's password
        :param role: (str) The user's role
        :return: (Response) The response object containing values corresponding to the request
        """
        return user_man.sign_up(self.project_id, self.db_type, self.token, self.stub, email, name, password, role)


__all__ = ['SQL']
