from typing import Optional, Dict, Any
from space_api.transport import make_meta, create
from space_api.proto.server_pb2_grpc import SpaceCloudStub


class Insert:
    """
    The Mongo Insert Interface
    ::
        from space_api import API
        api = API("My-Project", "localhost:8080")
        db = api.mongo()
        record = {'author': 'John', 'title': 'Title1'}
        response = db.insert('posts').doc(record).apply()

    :param project_id: (str) The project ID
    :param collection: (str) The collection name
    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param token: (str) The (optional) JWT Token
    :param operation: (str) The (optional) operation (one/all) (Defaults to 'all')
    """

    def __init__(self, project_id: str, collection: str, stub: SpaceCloudStub, token: Optional[str] = None,
                 operation: str = 'all'):
        self.project_id = project_id
        self.collection = collection
        self.stub = stub
        self.db_type = "mongo"
        self.token = token
        self.meta = make_meta(self.project_id, self.db_type, self.collection, self.token)
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

    def apply(self) -> Dict[str, Any]:
        """
        Triggers the insert request
        ::
            records = [{'author': 'John', 'title': 'Title1'}]
            response = db.insert('posts').docs(records).apply()

        :return: (Dict[str, Any]) The response dictionary
        """
        return create(self.stub, document=self.document, operation=self.operation, meta=self.meta)


__all__ = ['Insert']
