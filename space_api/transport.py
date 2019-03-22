import grpc
import json
from typing import Optional, Dict
from space_api.proto import server_pb2, server_pb2_grpc


def _obj_to_utf8_bytes(obj):
    return json.dumps(obj, separators=(',', ':')).encode('utf-8')


def _get_response_dict(response):
    ans = dict()
    ans["status"] = response.status
    ans["error"] = response.error
    ans["result"] = json.loads(response.result)
    return ans


def make_meta(project: str, db_type: str, col: str, token: Optional[str] = None) -> server_pb2.Meta:
    return server_pb2.Meta(project=project, dbType=db_type, col=col, token=token)


def make_read_options(select: Dict[str, int], sort: Dict[str, int], skip: int, limit: int,
                      distinct: str) -> server_pb2.ReadOptions:
    return server_pb2.ReadOptions(select=select, sort=sort, skip=skip, limit=limit, distinct=distinct)


def create(url: str, document, operation: str, meta: server_pb2.Meta):
    document = _obj_to_utf8_bytes(document)
    create_request = server_pb2.CreateRequest(document=document, operation=operation, meta=meta)
    with grpc.insecure_channel(url) as channel:
        stub = server_pb2_grpc.SpaceCloudStub(channel)
        return _get_response_dict(stub.Create(create_request))


def read(url: str, find, operation, options: server_pb2.ReadOptions, meta: server_pb2.Meta):
    find = _obj_to_utf8_bytes(find)
    read_request = server_pb2.ReadRequest(find=find, operation=operation, options=options, meta=meta)
    with grpc.insecure_channel(url) as channel:
        stub = server_pb2_grpc.SpaceCloudStub(channel)
        return _get_response_dict(stub.Read(read_request))


def update(url: str, find, operation: str, _update, meta: server_pb2.Meta):
    find = _obj_to_utf8_bytes(find)
    _update = _obj_to_utf8_bytes(_update)
    update_request = server_pb2.UpdateRequest(find=find, operation=operation, update=_update, meta=meta)
    with grpc.insecure_channel(url) as channel:
        stub = server_pb2_grpc.SpaceCloudStub(channel)
        return _get_response_dict(stub.Update(update_request))


def delete(url: str, find, operation: str, meta: server_pb2.Meta):
    find = _obj_to_utf8_bytes(find)
    delete_request = server_pb2.DeleteRequest(find=find, operation=operation, meta=meta)
    with grpc.insecure_channel(url) as channel:
        stub = server_pb2_grpc.SpaceCloudStub(channel)
        return _get_response_dict(stub.Delete(delete_request))


def aggregate(url: str, pipeline, operation: str, meta: server_pb2.Meta):
    pipeline = _obj_to_utf8_bytes(pipeline)
    aggregate_request = server_pb2.AggregateRequest(pipeline=pipeline, operation=operation, meta=meta)
    with grpc.insecure_channel(url) as channel:
        stub = server_pb2_grpc.SpaceCloudStub(channel)
        return _get_response_dict(stub.Aggregate(aggregate_request))
