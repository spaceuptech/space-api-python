from typing import Optional
from space_api.utils import generate_find, AND
from space_api.transport import make_meta, update
from space_api.proto.server_pb2_grpc import SpaceCloudStub
from space_api.response import Response


class Update:
    """
    The SQL Update Class
    ::
        from space_api import API, AND, OR, COND
        api = API("My-Project", "localhost:8080")
        db = api.my_sql() # For a MySQL interface
        response = db.update('posts').where(AND(COND('title', '==', 'Title1'))).set({'title':'Title2'}).apply()

    :param project_id: (str) The project ID
    :param collection: (str) The collection name
    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param db_type: (str) The database type
    :param token: (str) The (optional) JWT Token
    :param operation: (str) The (optional) operation (one/all) (Defaults to 'all')
    """

    def __init__(self, project_id: str, collection: str, stub: SpaceCloudStub, db_type: str,
                 token: Optional[str] = None, operation: str = 'all'):
        self.project_id = project_id
        self.collection = collection
        self.stub = stub
        self.db_type = db_type
        self.token = token
        self.params = {'find': {}, 'update': {}}
        self.meta = make_meta(self.project_id, self.db_type, self.collection, self.token)
        self.operation = operation

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
        return update(self.stub, find=self.params['find'], operation=self.operation, _update=self.params['update'],
                      meta=self.meta)


__all__ = ['Update']
