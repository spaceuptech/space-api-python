from typing import Optional, Dict, Any
from space_api.utils import generate_find, AND
from space_api.transport import make_meta, delete
from space_api.proto.server_pb2_grpc import SpaceCloudStub


class Delete:
    """
    The SQL Delete Interface
    ::
        from space_api import API, AND, OR, COND
        api = API("My-Project", "localhost:8080")
        db = api.my_sql() # For a MySQL interface
        response = db.delete('posts').where(AND(COND('title', '==', 'Title1'))).all()

    :param project_id: (str) The project ID
    :param collection: (str) The collection name
    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param db_type: (str) The database type
    :param token: (str) The (optional) JWT Token
    """

    def __init__(self, project_id: str, collection: str, stub: SpaceCloudStub, db_type: str,
                 token: Optional[str] = None):
        self.project_id = project_id
        self.collection = collection
        self.stub = stub
        self.db_type = db_type
        self.token = token
        self.params = {'find': {}}
        self.meta = make_meta(self.project_id, self.db_type, self.collection, self.token)

    def where(self, *conditions) -> 'Delete':
        """
        Prepares the find parameters

        :param conditions: (*) The conditions to find by
        """
        self.params['find'] = generate_find(AND(*conditions))
        return self

    def all(self) -> Dict[str, Any]:
        """
        Deletes all matching records

        :return: (dict{str:Any})  The response dictionary
        """
        return delete(self.stub, find=self.params['find'], operation='all', meta=self.meta)


__all__ = ['Delete']
