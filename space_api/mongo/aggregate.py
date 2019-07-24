from space_api.transport import Transport
from space_api.response import Response


class Aggregate:
    """
    The Mongo Aggregate Class
    ::
        from space_api import API, AND, OR, COND
        api = API("My-Project", "localhost:4124")
        db = api.mongo()
        _pipe = [
            {'$match': {'status': 'A'}},
            {'$group': {'_id': '$customer_id', 'total': {'$sum': '$amount'}}}
        ]
        response = db.aggr('posts').pipe(_pipe).apply()

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
        self.params = {}

    def pipe(self, pipe_obj) -> 'Aggregate':
        """
        Prepares the pipe query

        :param pipe_obj: The pipeline object
        """
        self.params['pipe'] = pipe_obj
        return self

    def apply(self) -> Response:
        """
        Triggers the aggregate request
        ::
            response = db.aggr('posts').pipe([...]).apply()

        :return: (Response) The response object containing values corresponding to the request
        """
        return self.transport.aggregate(self.params['pipe'], self.operation, self.db_type, self.collection)


__all__ = ['Aggregate']
