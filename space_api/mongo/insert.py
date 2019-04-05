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
        response = db.insert('posts').one(record)

    :param project_id: (str) The project ID
    :param collection: (str) The collection name
    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param token: (str) The (optional) JWT Token
    """

    def __init__(self, project_id: str, collection: str, stub: SpaceCloudStub, token: Optional[str] = None):
        self.project_id = project_id
        self.collection = collection
        self.stub = stub
        self.db_type = "mongo"
        self.token = token
        self.meta = make_meta(self.project_id, self.db_type, self.collection, self.token)

    def one(self, record) -> Dict[str, Any]:
        """
        Inserts a single record
        ::
            record = {'author': 'John', 'title': 'Title1'}
            response = db.insert('posts').one(record)

        :param record: The record to insert
        :return: (dict{str:Any}) The response dictionary
        """
        return create(self.stub, document=record, operation='one', meta=self.meta)

    def all(self, records) -> Dict[str, Any]:
        """
        Inserts multiple records
        ::
            records = [{'author': 'John', 'title': 'Title1'}]
            response = db.insert('posts').all(records)

        :param records: (list) The records to insert
        :return: (dict{str:Any}) The response dictionary
        """
        return create(self.stub, document=records, operation='all', meta=self.meta)


__all__ = ['Insert']
