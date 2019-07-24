from space_api.transport import Transport
from space_api.response import Response


class Insert:
    """
    The Mongo Insert Class
    ::
        from space_api import API
        api = API("My-Project", "localhost:4124")
        db = api.mongo()
        record = {'author': 'John', 'title': 'Title1'}
        response = db.insert('posts').doc(record).apply()

    :param transport: (Transport) The API's transport instance
    :param collection: (str) The collection name
    :param db_type: (str) The database type
    :param operation: (str) The (optional) operation (one/all/distinct/count) (Defaults to 'all')
    """

    def __init__(self, transport: Transport, collection: str, db_type: str, operation: str = 'all'):
        self.transport = transport
        self.collection = collection
        self.db_type = db_type
        self.operation = operation
        self.document = None

    def doc(self, record) -> 'Insert':
        """
        Sets the record to insert
        ::
            record = {'author': 'John', 'title': 'Title1'}
            response = db.insert('posts').doc(record).apply()

        :param record: The record to insert
        """
        self.operation = 'one'
        self.document = record
        return self

    def docs(self, records) -> 'Insert':
        """
        Sets the records to insert
        ::
            records = [{'author': 'John', 'title': 'Title1'}]
            response = db.insert('posts').docs(records).apply()

        :param records: The records to insert
        """
        self.operation = 'all'
        self.document = records
        return self

    def apply(self) -> Response:
        """
        Triggers the insert request
        ::
            records = [{'author': 'John', 'title': 'Title1'}]
            response = db.insert('posts').docs(records).apply()

        :return: (Response) The response object containing values corresponding to the request
        """
        return self.transport.create(self.document, self.operation, self.db_type, self.collection)


__all__ = ['Insert']
