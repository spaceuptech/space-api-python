from space_api.utils import generate_find, AND
from space_api.transport import Transport
from space_api.response import Response


class Update:
    """
    The SQL Update Class
    ::
        from space_api import API, AND, OR, COND
        api = API("My-Project", "localhost:4124")
        db = api.my_sql() # For a MySQL interface
        response = db.update('posts').where(AND(COND('title', '==', 'Title1'))).set({'title':'Title2'}).apply()

    :param transport: (Transport) The API's transport instance
    :param collection: (str) The collection name
    :param db_type: (str) The database type
    :param operation: (str) The (optional) operation (one/all/upsert) (Defaults to 'all')
    """

    def __init__(self, transport: Transport, collection: str, db_type: str, operation: str = 'all'):
        self.transport = transport
        self.collection = collection
        self.db_type = db_type
        self.operation = operation
        self.params = {'find': {}, 'update': {}}

    def where(self, *conditions) -> 'Update':
        """
        Prepares the find parameters

        :param conditions: (*) The conditions to find by
        """
        self.params['find'] = generate_find(AND(*conditions))
        return self

    def set(self, obj) -> 'Update':
        """
        Prepares the updated values

        :param obj: The object containing the fields to set
        """
        self.params['update']['$set'] = obj
        return self

    def apply(self) -> Response:
        """
        Triggers the update request

        :return: (Response) The response object containing values corresponding to the request
        """
        return self.transport.update(self.params['find'], self.operation, self.params['update'], self.db_type,
                                     self.collection)


__all__ = ['Update']
