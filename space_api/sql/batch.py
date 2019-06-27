from typing import Union
from space_api.transport import Transport
from space_api.utils import obj_to_utf8_bytes
from space_api.proto import server_pb2
from space_api.sql.delete import Delete
from space_api.sql.insert import Insert
from space_api.sql.update import Update


class Batch:
    """
    The SQL Batch Class
    ::
        from space_api import API, AND, OR, COND
        api = API("My-Project", "localhost:8080")
        db = api.my_sql() # For a MySQL interface

    :param transport: (Transport) The API's transport instance
    :param db_type: (str) The database type
    """

    def __init__(self, transport: Transport, db_type: str):
        self.transport = transport
        self.db_type = db_type
        self.requests = []

    def add(self, request: Union[Insert, Update, Delete]):
        """
        Adds a request to the batch request object
        ::
            batch_object.add(db.delete('books').where(COND('name', '!=', 'Book_name')))
        
        :param request: (Insert or Update or Delete) A request to add to the batch request
        """
        if self.db_type != request.db_type:
            raise Exception("Cannot Batch Requests of Different Database Types")
        all_request = server_pb2.AllRequest()
        if isinstance(request, Insert):
            all_request.col = request.collection
            all_request.document = obj_to_utf8_bytes(request.document)
            all_request.operation = request.operation
            all_request.type = "create"
        if isinstance(request, Update):
            all_request.col = request.collection
            all_request.operation = request.operation
            all_request.find = obj_to_utf8_bytes(request.params['find'])
            all_request.update = obj_to_utf8_bytes(request.params['update'])
            all_request.type = "update"
        if isinstance(request, Delete):
            all_request.col = request.collection
            all_request.operation = request.operation
            all_request.find = obj_to_utf8_bytes(request.params['find'])
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
        return self.transport.batch(self.requests, self.db_type)


__all__ = ['Batch']
