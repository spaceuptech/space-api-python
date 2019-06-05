from typing import Optional, Union
from space_api.transport import make_meta, batch, _obj_to_utf8_bytes
from space_api.proto import server_pb2
from space_api.proto.server_pb2_grpc import SpaceCloudStub
from space_api.sql.delete import Delete
from space_api.sql.insert import Insert
from space_api.sql.update import Update


class Batch:
    """
    The SQL Batch Interface
    ::
        from space_api import API, AND, OR, COND
        api = API("My-Project", "localhost:8080")
        db = api.my_sql() # For a MySQL interface

    :param project_id: (str) The project ID
    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param db_type: (str) The database type
    :param token: (str) The (optional) JWT Token
    """

    def __init__(self, project_id: str, stub: SpaceCloudStub, db_type: str, token: Optional[str] = None):
        self.project_id = project_id
        self.stub = stub
        self.db_type = db_type
        self.token = token
        self.requests = []
        self.meta = make_meta(self.project_id, self.db_type, None, self.token)

    def add(self, request: Union[Insert, Update, Delete]):
        """
        Adds a request to the batch request object
        ::
            batch_object.add(db.delete('books').where(COND('name', '!=', 'Book_name')))
        
        :param request: (Insert or Update or Delete) A request to add to the batch request
        """
        if self.project_id != request.project_id:
            raise Exception("Cannot Batch Requests of Different Projects")
        if self.db_type != request.db_type:
            raise Exception("Cannot Batch Requests of Different Database Types")
        if self.token != request.token:
            raise Exception("Cannot Batch Requests using Different Tokens")
        all_request = server_pb2.AllRequest()
        if isinstance(request, Insert):
            all_request.col = request.collection
            all_request.document = _obj_to_utf8_bytes(request.document)
            all_request.operation = request.operation
            all_request.type = "create"
        if isinstance(request, Update):
            all_request.col = request.collection
            all_request.operation = request.operation
            all_request.find = _obj_to_utf8_bytes(request.params['find'])
            all_request.update = _obj_to_utf8_bytes(request.params['update'])
            all_request.type = "update"
        if isinstance(request, Delete):
            all_request.col = request.collection
            all_request.operation = request.operation
            all_request.find = _obj_to_utf8_bytes(request.params['find'])
            all_request.type = "delete"
        self.requests.append(all_request)
        return self

    def apply(self):
        """
        Triggers the batch request
        ::
            batch_obj = db.begin_batch()
            batch_obj.add(...)
            response = batch_obj.apply()

        :return: (Response) The response object containing values corresponding to the request
        """
        return batch(self.stub, self.requests, meta=self.meta)


__all__ = ['Batch']
