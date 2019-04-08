from typing import Optional, Dict, Any
from space_api.transport import make_meta, aggregate
from space_api.proto.server_pb2_grpc import SpaceCloudStub


class Aggregate:
    """
    The Mongo Aggregate Interface
    ::
        from space_api import API, AND, OR, COND
        api = API("My-Project", "localhost:8080")
        db = api.mongo()
        _pipe = [
            {'$match': {'status': 'A'}},
            {'$group': {'_id': '$customer_id', 'total': {'$sum': '$amount'}}}
        ]
        response = db.aggr('posts').pipe(_pipe).apply()

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
        self.params = {}
        self.meta = make_meta(self.project_id, self.db_type, self.collection, self.token)
        self.operation = operation

    def pipe(self, pipe_obj) -> 'Aggregate':
        """
        Prepares the pipe query

        :param pipe_obj: The pipeline object
        """
        self.params['pipe'] = pipe_obj
        return self

    def apply(self) -> Dict[str, Any]:
        """
        Triggers the aggregate request
        ::
            response = db.aggr('posts').pipe([...]).apply()

        :return: (dict{str:Any})  The response dictionary
        """
        return aggregate(self.stub, pipeline=self.params['pipe'], operation=self.operation, meta=self.meta)


__all__ = ['Aggregate']
