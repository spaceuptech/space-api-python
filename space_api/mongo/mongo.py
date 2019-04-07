from typing import Optional
from space_api.proto.server_pb2_grpc import SpaceCloudStub
from space_api.mongo.get import Get
from space_api.mongo.insert import Insert
from space_api.mongo.update import Update
from space_api.mongo.delete import Delete
from space_api.mongo.aggregate import Aggregate


class Mongo:
    """
    The Mongo Client Interface
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


__all__ = ['Mongo']
