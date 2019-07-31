from typing import Optional
from space_api.transport import Transport
from space_api.db.get import Get
from space_api.db.insert import Insert
from space_api.db.update import Update
from space_api.db.delete import Delete
from space_api.db.aggregate import Aggregate
from space_api.db.batch import Batch
from space_api.response import Response
from space_api.livequery import LiveQuery


class DB:
    """
    The DB Client Class
    ::
        from space_api import API
        api = API("My-Project", "localhost:4124")
        db = api.mongo()  # For a MongoDB interface

    :param transport: (Transport) The API's transport instance
    :param db_type: (str) The database type
    """

    def __init__(self, transport: Transport, db_type: str):
        self.transport = transport
        self.db_type = db_type

    def get(self, collection: str) -> 'Get':
        """
        Returns a DB Get object, with operation 'all'

        :param collection: (str) The collection name
        :return: The DB Get object
        """
        return Get(self.transport, collection, self.db_type)

    def get_one(self, collection: str) -> 'Get':
        """
        Returns a DB Get object, with operation 'one'

        :param collection: (str) The collection name
        :return: The DB Get object
        """
        return Get(self.transport, collection, self.db_type, operation='one')

    def count(self, collection: str) -> 'Get':
        """
        Returns a DB Get object, with operation 'count'
        ::
            response = db.count('posts').apply()

        :param collection: (str) The collection name
        :return: The DB Get object
        """
        return Get(self.transport, collection, self.db_type, operation='count')

    def distinct(self, collection: str) -> 'Get':
        """
        Returns a DB Get object, with operation 'distinct'
        ::
            response = db.distinct('post').key('category').apply()

        :param collection: (str) The collection name
        :return: The DB Get object
        """
        return Get(self.transport, collection, self.db_type, operation='distinct')

    def insert(self, collection: str) -> 'Insert':
        """
        Returns a DB Insert object

        :param collection: (str) The collection name
        :return: The DB Insert object
        """
        return Insert(self.transport, collection, self.db_type)

    def update(self, collection: str) -> 'Update':
        """
        Returns a DB Update object, with operation 'all'

        :param collection: (str) The collection name
        :return: The DB Update object
        """
        return Update(self.transport, collection, self.db_type)

    def update_one(self, collection: str) -> 'Update':
        """
        Returns a DB Update object, with operation 'one'

        :param collection: (str) The collection name
        :return: The DB Update object
        """
        return Update(self.transport, collection, self.db_type, operation='one')

    def upsert(self, collection: str) -> 'Update':
        """
        Returns a DB Update object, with operation 'upsert'

        :param collection: (str) The collection name
        :return: The DB Update object
        """
        return Update(self.transport, collection, self.db_type, operation='upsert')

    def delete(self, collection: str) -> 'Delete':
        """
        Returns a DB Delete object, with operation 'all'

        :param collection: (str) The collection name
        :return: The DB Delete object
        """
        return Delete(self.transport, collection, self.db_type)

    def delete_one(self, collection: str) -> 'Delete':
        """
        Returns a DB Delete object, with operation 'one'

        :param collection: (str) The collection name
        :return: The DB Delete object
        """
        return Delete(self.transport, collection, self.db_type, operation='one')

    def aggr(self, collection: str) -> 'Aggregate':
        """
        Returns a DB Aggregate object, with operation 'all'

        :param collection: (str) The collection name
        :return: The DB Aggregate object
        """
        return Aggregate(self.transport, collection, self.db_type)

    def aggr_one(self, collection: str) -> 'Aggregate':
        """
        Returns a DB Aggregate object, with operation 'one'

        :param collection: (str) The collection name
        :return: The DB Aggregate object
        """
        return Aggregate(self.transport, collection, self.db_type, operation='one')

    def begin_batch(self) -> 'Batch':
        """
        Creates a Batch request
        ::
            batch_obj = db.begin_batch()
            batch_obj.add(...)
            response = batch_obj.apply()

        :return: (Batch) A DB Batch object
        """
        return Batch(self.transport, self.db_type)

    def live_query(self, collection: str) -> LiveQuery:
        """
        Returns a DB LiveQuery object

        :param collection: (str) The collection name
        :return: The DB LiveQuery object
        """
        return LiveQuery(self.transport, self.db_type, collection)

    def profile(self, _id: str) -> Response:
        """
        Gets the profile of the user
        ::
            response = db.profile("user_id")

        :param _id: (str) The user's id
        :return: (Response) The response object containing values corresponding to the request
        """
        return self.transport.profile(_id, self.db_type)

    def profiles(self) -> Response:
        """
        Gets the all the profiles
        ::
            response = db.profile()

        :return: (Response) The response object containing values corresponding to the request
        """
        return self.transport.profiles(self.db_type)

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
        return self.transport.edit_profile(_id, email, name, password, self.db_type)

    def sign_in(self, email: str, password: str) -> Response:
        """
        Allows the user to sign in
        ::
            response = db.sign_in("user_email", "user_password")

        :param email: (str) The user's email id
        :param password: (str) The user's password
        :return: (Response) The response object containing values corresponding to the request
        """
        return self.transport.sign_in(email, password, self.db_type)

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
        return self.transport.sign_up(email, name, password, role, self.db_type)


__all__ = ['DB']
