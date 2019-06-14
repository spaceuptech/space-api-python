from typing import Optional
from space_api.proto.server_pb2_grpc import SpaceCloudStub
from space_api.mongo.get import Get
from space_api.mongo.insert import Insert
from space_api.mongo.update import Update
from space_api.mongo.delete import Delete
from space_api.mongo.aggregate import Aggregate
from space_api.mongo.batch import Batch
from space_api.response import Response
from space_api import user_man
from space_api.realtime import Realtime
from space_api.livequery import LiveQuery


class Mongo:
    """
    The Mongo Client Class
    ::
        from space_api import API
        api = API("My-Project", "localhost:8080")
        db = api.mongo()

    :param project_id: (str) The project ID
    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param token: (str) The (optional) JWT Token
    """

    def __init__(self, project_id: str, stub: SpaceCloudStub, token: Optional[str] = None):
        self.project_id = project_id
        self.stub = stub
        self.db_type = "mongo"
        self.token = token
        self.realtime = Realtime(project_id, self.stub, self.db_type, self.token)

    def get(self, collection: str) -> 'Get':
        """
        Returns a Mongo Get object, with operation 'all'

        :param collection: (str) The collection name
        :return: The Mongo Get object
        """
        return Get(self.project_id, collection, self.stub, self.token)

    def get_one(self, collection: str) -> 'Get':
        """
        Returns a Mongo Get object, with operation 'one'

        :param collection: (str) The collection name
        :return: The Mongo Get object
        """
        return Get(self.project_id, collection, self.stub, self.token, operation='one')

    def count(self, collection: str) -> 'Get':
        """
        Returns a Mongo Get object, with operation 'count'
        ::
            response = db.count('posts').apply()

        :param collection: (str) The collection name
        :return: The Mongo Get object
        """
        return Get(self.project_id, collection, self.stub, self.token, operation='count')

    def distinct(self, collection: str) -> 'Get':
        """
        Returns a Mongo Get object, with operation 'distinct'
        ::
            response = db.distinct('post').key('category').apply()

        :param collection: (str) The collection name
        :return: The Mongo Get object
        """
        return Get(self.project_id, collection, self.stub, self.token, operation='distinct')

    def insert(self, collection: str) -> 'Insert':
        """
        Returns a Mongo Insert object

        :param collection: (str) The collection name
        :return: The Mongo Insert object
        """
        return Insert(self.project_id, collection, self.stub, self.token)

    def update(self, collection: str) -> 'Update':
        """
        Returns a Mongo Update object, with operation 'all'

        :param collection: (str) The collection name
        :return: The Mongo Update object
        """
        return Update(self.project_id, collection, self.stub, self.token)

    def update_one(self, collection: str) -> 'Update':
        """
        Returns a Mongo Update object, with operation 'one'

        :param collection: (str) The collection name
        :return: The Mongo Update object
        """
        return Update(self.project_id, collection, self.stub, self.token, operation='one')

    def upsert(self, collection: str) -> 'Update':
        """
        Returns a Mongo Update object, with operation 'upsert'

        :param collection: (str) The collection name
        :return: The Mongo Update object
        """
        return Update(self.project_id, collection, self.stub, self.token, operation='upsert')

    def delete(self, collection: str) -> 'Delete':
        """
        Returns a Mongo Delete object, with operation 'all'

        :param collection: (str) The collection name
        :return: The Mongo Delete object
        """
        return Delete(self.project_id, collection, self.stub, self.token)

    def delete_one(self, collection: str) -> 'Delete':
        """
        Returns a Mongo Delete object, with operation 'one'

        :param collection: (str) The collection name
        :return: The Mongo Delete object
        """
        return Delete(self.project_id, collection, self.stub, self.token, operation='one')

    def aggr(self, collection: str) -> 'Aggregate':
        """
        Returns a Mongo Aggregate object, with operation 'all'

        :param collection: (str) The collection name
        :return: The Mongo Aggregate object
        """
        return Aggregate(self.project_id, collection, self.stub, self.token)

    def aggr_one(self, collection: str) -> 'Aggregate':
        """
        Returns a Mongo Aggregate object, with operation 'one'

        :param collection: (str) The collection name
        :return: The Mongo Aggregate object
        """
        return Aggregate(self.project_id, collection, self.stub, self.token, operation='one')

    def begin_batch(self) -> 'Batch':
        """
        Creates a Batch request
        ::
            batch_obj = db.begin_batch()
            batch_obj.add(...)
            response = batch_obj.apply()

        :return: (Batch) A Mongo Batch object
        """
        return Batch(self.project_id, self.stub, self.db_type, self.token)

    def live_query(self, collection: str) -> LiveQuery:
        """
        Returns a Mongo LiveQuery object

        :param collection: (str) The collection name
        :return: The Mongo LiveQuery object
        """
        return self.realtime.live_query(collection)

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


__all__ = ['Mongo']
