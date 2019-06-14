from typing import Optional
from space_api.livequery import LiveQuery
from space_api.proto.server_pb2_grpc import SpaceCloudStub


class Realtime:
    """
    The Realtime Class (Used internally only)
    ::
        from space_api import API
        api = API('project', 'localhost:8081')
        db = api.my_sql()

        realtime = Realtime(project_id, self.stub, self.db_type, self.token)

    :param project_id: (str) The project ID
    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param db_type: (str) The database type
    :param token: (str) The (optional) JWT Token
    """

    def __init__(self, project_id: str, stub: SpaceCloudStub, db_type:str, token: Optional[str]=None):
        self.stub = stub
        self.project_id = project_id
        self.db_type = db_type
        self.token = token
        self.store = {}
        # TODO Register Callbacks for Reconnect

    def live_query(self, collection) -> 'LiveQuery':
        """
        Returns a LiveQuery object
        :param collection: (str) The collection name
        :return: (LiveQuery) The LiveQuery object
        """
        return LiveQuery(self.project_id, self.stub, self.db_type, collection, self.store, self.token)


__all__ = ['Realtime']
