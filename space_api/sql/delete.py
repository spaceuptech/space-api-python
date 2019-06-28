from space_api.utils import generate_find, AND
from space_api.transport import Transport
from space_api.response import Response


class Delete:
    """
    The SQL Delete Class
    ::
        from space_api import API, AND, OR, COND
        api = API("My-Project", "localhost:8080")
        db = api.my_sql() # For a MySQL interface
        response = db.delete('posts').where(AND(COND('title', '==', 'Title1'))).apply()

    :param transport: (Transport) The API's transport instance
    :param collection: (str) The collection name
    :param db_type: (str) The database type
    :param operation: (str) The (optional) operation (one/all) (Defaults to 'all')
    """

    def __init__(self, transport: Transport, collection: str, db_type: str, operation: str = 'all'):
        self.transport = transport
        self.collection = collection
        self.db_type = db_type
        self.operation = operation
        self.params = {'find': {}}

    def where(self, *conditions) -> 'Delete':
        """
        Prepares the find parameters

        :param conditions: (*) The conditions to find by
        """
        self.params['find'] = generate_find(AND(*conditions))
        return self

    def apply(self) -> Response:
        """
        Triggers the delete request

        :return: (Response) The response object containing values corresponding to the request
        """
        return self.transport.delete(self.params['find'], self.operation, self.db_type, self.collection)


__all__ = ['Delete']
