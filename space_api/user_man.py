from typing import Optional
from space_api.proto.server_pb2_grpc import SpaceCloudStub
from space_api import transport


def profile(project_id: str, db_type: str, token: str, stub: SpaceCloudStub, _id: str):
    """
    Triggers the profile request

    :param project_id: (str) The project ID
    :param db_type: (str) The database type
    :param token: (str) The (optional) JWT Token
    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param _id: (str) The user's id
    :return: (Response) The response object containing values corresponding to the request
    """
    meta = transport.make_meta(project_id, db_type, None, token)
    return transport.profile(stub, _id, meta)


def profiles(project_id: str, db_type: str, token: str, stub: SpaceCloudStub):
    """
    Triggers the profiles request

    :param project_id: (str) The project ID
    :param db_type: (str) The database type
    :param token: (str) The (optional) JWT Token
    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :return: (Response) The response object containing values corresponding to the request
    """
    meta = transport.make_meta(project_id, db_type, None, token)
    return transport.profiles(stub, meta)


def edit_profile(project_id: str, db_type: str, token: str, stub: SpaceCloudStub, _id: str, email: Optional[str] = None,
                 name: Optional[str] = None, password: Optional[str] = None):
    """
    Triggers the edit_profile request

    :param project_id: (str) The project ID
    :param db_type: (str) The database type
    :param token: (str) The (optional) JWT Token
    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param _id: (str) The user's id
    :param email: (str) The (optional) new email id
    :param name: (str) Then (optional) new name
    :param password: (str) The (optional) new password
    :return: (Response) The response object containing values corresponding to the request
    """
    meta = transport.make_meta(project_id, db_type, None, token=token)
    return transport.edit_profile(stub, _id, email=email, name=name, password=password, meta=meta)


def sign_in(project_id: str, db_type: str, token: str, stub: SpaceCloudStub, email: str, password: str):
    """
    Triggers the sign_in request

    :param project_id: (str) The project ID
    :param db_type: (str) The database type
    :param token: (str) The (optional) JWT Token
    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param email: (str) The user's email id
    :param password: (str) The user's password
    :return: (Response) The response object containing values corresponding to the request
    """
    meta = transport.make_meta(project_id, db_type, None, token)
    return transport.sign_in(stub, email, password, meta)


def sign_up(project_id: str, db_type: str, token: str, stub: SpaceCloudStub, email: str, name: str, password: str,
            role: str):
    """
    Triggers the sign_in request

    :param project_id: (str) The project ID
    :param db_type: (str) The database type
    :param token: (str) The (optional) JWT Token
    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param email: (str) The user's email id
    :param name: (str) The user's name
    :param password: (str) The user's password
    :param role: (str) The user's role
    :return: (Response) The response object containing values corresponding to the request
    """
    meta = transport.make_meta(project_id, db_type, None, token)
    return transport.sign_up(stub, email, name, password, role, meta)
