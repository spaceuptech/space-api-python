from typing import Optional, Dict, Any
from space_api.utils import generate_find, AND
from space_api.transport import make_meta, delete
from space_api.proto.server_pb2_grpc import SpaceCloudStub


class Delete:
    """
    The Mongo Delete Interface
    ::
        from space_api import API, AND, OR, COND
        api = API("My-Project", "localhost:8080")
        db = api.mongo()
        response = db.delete('posts').where(AND(COND('title', '==', 'Title1'))).apply()

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
        self.params = {'find': {}}
        self.meta = make_meta(self.project_id, self.db_type, self.collection, self.token)
        self.operation = operation

    def where(self, *conditions) -> 'Delete':
        """
        Prepares the find parameters

        :param conditions: (*) The conditions to find by
        """
        self.params['find'] = generate_find(AND(*conditions))
        return self

    def apply(self) -> Dict[str, Any]:
        """
        Triggers the delete request

        :return: (Dict[str, Any])  The response dictionary
        """
        return delete(self.stub, find=self.params['find'], operation=self.operation, meta=self.meta)


__all__ = ['Delete']
