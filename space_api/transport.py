import json
from typing import Optional, Dict
from space_api.proto import server_pb2, server_pb2_grpc
from space_api.response import Response


def _obj_to_utf8_bytes(obj) -> bytes:
    """
    Converts a JavaScript object-like variable into utf-8 bytes
    :param obj: A JavaScript object-like variable 
    :return: (bytes) The utf-8 bytes of the object
    """
    return json.dumps(obj, separators=(',', ':')).encode(encoding='utf-8')


def make_meta(project: str, db_type: str, col: str, token: Optional[str] = None) -> server_pb2.Meta:
    """
    Makes a gRPC Meta object

    :param project: (str) The project id
    :param db_type: (str) The database type
    :param col: (str) The collection name
    :param token: (str) The (optional) JWT Token
    :return: (server_pb2.Meta) gRPC Meta object
    """
    return server_pb2.Meta(project=project, dbType=db_type, col=col, token=token)


def make_read_options(select: Dict[str, int], sort: Dict[str, int], skip: int, limit: int,
                      distinct: str) -> server_pb2.ReadOptions:
    """
    Makes a gRPC ReadOptions object

    :param select: (dict{str:int}) The select parameters
    :param sort: (dict{str:int}) The sort parameters
    :param skip: (int) The number of records to skip
    :param limit: (int) The maximum number of results returned
    :param distinct: (str) Get distinct results only
    :return: (server_pb2.ReadOptions) gRPC ReadOptions object
    """
    return server_pb2.ReadOptions(select=select, sort=sort, skip=skip, limit=limit, distinct=distinct)


def create(stub: server_pb2_grpc.SpaceCloudStub, document, operation: str, meta: server_pb2.Meta) -> Response:
    """
    Calls the gRPC Create function

    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param document: The document to create
    :param operation: (str) The operation to perform
    :param meta: (server_pb2.Meta) The gRPC Meta object
    :return: (Response) The response object containing values corresponding to the request
    """
    document = _obj_to_utf8_bytes(document)
    create_request = server_pb2.CreateRequest(document=document, operation=operation, meta=meta)
    return Response(stub.Create(create_request))


def faas(stub: server_pb2_grpc.SpaceCloudStub, params, timeout: int, service: str, function: str,
             token: str) -> Response:
    """
    Calls the gRPC Call function

    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param params: The params for the function
    :param timeout: (int) The (optional) timeout in milliseconds (defaults to 5000)
    :param service: (str) The name of service (engine) with which the function is registered
    :param function: (str) The name of function to be called
    :param token: (str) The signed JWT token received from the server on successful authentication
    :return: (Response) The response object containing values corresponding to the request
    """
    params = _obj_to_utf8_bytes(params)
    function_request = server_pb2.FunctionsRequest(params=params, timeout=timeout, service=service, function=function,
                                                   token=token)
    return Response(stub.Call(function_request))


def read(stub: server_pb2_grpc.SpaceCloudStub, find, operation: str, options: server_pb2.ReadOptions,
         meta: server_pb2.Meta) -> Response:
    """
    Calls the gRPC Read function
    
    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub 
    :param find: The find parameters
    :param operation: (str) The operation to perform
    :param options: (server_pb2.ReadOptions) 
    :param meta: (server_pb2.Meta) The gRPC Meta object
    :return: (Response) The response object containing values corresponding to the request
    """
    find = _obj_to_utf8_bytes(find)
    read_request = server_pb2.ReadRequest(find=find, operation=operation, options=options, meta=meta)
    return Response(stub.Read(read_request))


def update(stub: server_pb2_grpc.SpaceCloudStub, find, operation: str, _update, meta: server_pb2.Meta) -> \
        Response:
    """
    Calls the gRPC Update function

    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param find: The find parameters
    :param operation: (str) The operation to perform
    :param _update: The update parameters
    :param meta: (server_pb2.Meta) The gRPC Meta object
    :return: (Response) The response object containing values corresponding to the request
    """
    find = _obj_to_utf8_bytes(find)
    _update = _obj_to_utf8_bytes(_update)
    update_request = server_pb2.UpdateRequest(find=find, operation=operation, update=_update, meta=meta)
    return Response(stub.Update(update_request))


def delete(stub: server_pb2_grpc.SpaceCloudStub, find, operation: str, meta: server_pb2.Meta) -> Response:
    """
    Calls the gRPC Delete function

    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param find: The find parameters
    :param operation: (str) The operation to perform
    :param meta: (server_pb2.Meta) The gRPC Meta object
    :return: (Response) The response object containing values corresponding to the request
    """
    find = _obj_to_utf8_bytes(find)
    delete_request = server_pb2.DeleteRequest(find=find, operation=operation, meta=meta)
    return Response(stub.Delete(delete_request))


def aggregate(stub: server_pb2_grpc.SpaceCloudStub, pipeline, operation: str, meta: server_pb2.Meta) -> Response:
    """
    Calls the gRPC Aggregate function

    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param pipeline: The pipeline parameters
    :param operation: (str) The operation to perform
    :param meta: (server_pb2.Meta) The gRPC Meta object
    :return: (Response) The response object containing values corresponding to the request
    """
    pipeline = _obj_to_utf8_bytes(pipeline)
    aggregate_request = server_pb2.AggregateRequest(pipeline=pipeline, operation=operation, meta=meta)
    return Response(stub.Aggregate(aggregate_request))
