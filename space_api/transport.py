import grpc
import io
from typing import Optional, Dict, List
from space_api.proto import server_pb2
from space_api.utils import obj_to_utf8_bytes
from space_api.proto.server_pb2_grpc import SpaceCloudStub
from space_api.response import Response
from space_api import constants


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


class Transport:
    """
        The SpaceUp Transport Instance
        ::
            transport = Transport("localhost:4124")

        :param url: (str) The URL of space-cloud server

        """

    def __init__(self, url: str, project_id: str, token: Optional[str] = None):
        self.url = url
        self.project_id = project_id
        self.token = token
        self.channel = grpc.insecure_channel(self.url)
        # self.channel = grpc.insecure_channel(self.url, options=[('grpc.keepalive_timeout_ms', 10000),
        #                                                         ('grpc.keepalive_permit_without_calls', 1)])
        self.stub = SpaceCloudStub(self.channel)

    def close(self):
        """
        Closes the communication channel
        """
        self.channel.close()

    def connect(self):
        """
        Connects to the Space Cloud Instance
        """
        self.channel = grpc.insecure_channel(self.url)
        self.stub = SpaceCloudStub(self.channel)

    def faas(self, service: str, function: str, params, timeout: int) -> Response:
        """
        Calls the gRPC Call function

        :param service: (str) The name of service(engine) with which the function is registered
        :param function: (str) The name of function to be called
        :param params: The params for the function
        :param timeout: (int) The timeout in milliseconds
        :return: (Response) The response object containing values corresponding to the request
        """
        params = obj_to_utf8_bytes(params)
        functions_request = server_pb2.FunctionsRequest(params=params, timeout=timeout // 1000, service=service,
                                                        function=function, token=self.token, project=self.project_id)
        return Response(self.stub.Call(functions_request))

    def _make_meta(self, db_type: Optional[str] = None, col: Optional[str] = None) -> server_pb2.Meta:
        """
        Makes a gRPC Meta object

        :param db_type: (str) The database type
        :param col: (str) The (optional) collection name
        :return: (server_pb2.Meta) gRPC Meta object
        """
        meta = server_pb2.Meta(project=self.project_id)
        if self.token is not None:
            meta.token = self.token
        if db_type is not None:
            meta.dbType = db_type
        if col is not None:
            meta.col = col
        return meta

    def read(self, find, operation: str, options: server_pb2.ReadOptions, db_type: str, col: str) -> Response:
        """
        Calls the gRPC Read function

        :param find: The find parameters
        :param operation: (str) The operation to perform
        :param options: (server_pb2.ReadOptions)
        :param db_type: (str) The database type
        :param col: (str) The (optional) collection name
        :return: (Response) The response object containing values corresponding to the request
        """
        find = obj_to_utf8_bytes(find)
        meta = self._make_meta(db_type, col)
        read_request = server_pb2.ReadRequest(find=find, operation=operation, options=options, meta=meta)
        return Response(self.stub.Read(read_request))

    def create(self, document, operation: str, db_type: str, col: str) -> Response:
        """
        Calls the gRPC Create function

        :param document: The document to create
        :param operation: (str) The operation to perform
        :param db_type: (str) The database type
        :param col: (str) The (optional) collection name
        :return: (Response) The response object containing values corresponding to the request
        """
        document = obj_to_utf8_bytes(document)
        meta = self._make_meta(db_type, col)
        create_request = server_pb2.CreateRequest(document=document, operation=operation, meta=meta)
        return Response(self.stub.Create(create_request))

    def update(self, find, operation: str, _update, db_type: str, col: str) -> Response:
        """
        Calls the gRPC Update function

        :param find: The find parameters
        :param operation: (str) The operation to perform
        :param _update: The update parameters
        :param db_type: (str) The database type
        :param col: (str) The (optional) collection name
        :return: (Response) The response object containing values corresponding to the request
        """
        find = obj_to_utf8_bytes(find)
        _update = obj_to_utf8_bytes(_update)
        meta = self._make_meta(db_type, col)
        update_request = server_pb2.UpdateRequest(find=find, operation=operation, update=_update, meta=meta)
        return Response(self.stub.Update(update_request))

    def delete(self, find, operation: str, db_type: str, col: str) -> Response:
        """
        Calls the gRPC Delete function

        :param find: The find parameters
        :param operation: (str) The operation to perform
        :param db_type: (str) The database type
        :param col: (str) The (optional) collection name
        :return: (Response) The response object containing values corresponding to the request
        """
        find = obj_to_utf8_bytes(find)
        meta = self._make_meta(db_type, col)
        delete_request = server_pb2.DeleteRequest(find=find, operation=operation, meta=meta)
        return Response(self.stub.Delete(delete_request))

    def aggregate(self, pipeline, operation: str, db_type: str, col: str) -> Response:
        """
        Calls the gRPC Aggregate function

        :param pipeline: The pipeline parameters
        :param operation: (str) The operation to perform
        :param db_type: (str) The database type
        :param col: (str) The (optional) collection name
        :return: (Response) The response object containing values corresponding to the request
        """
        pipeline = obj_to_utf8_bytes(pipeline)
        meta = self._make_meta(db_type, col)
        aggregate_request = server_pb2.AggregateRequest(pipeline=pipeline, operation=operation, meta=meta)
        return Response(self.stub.Aggregate(aggregate_request))

    def batch(self, all_requests: List[server_pb2.AllRequest], db_type: str) -> Response:
        """
        Calls the gRPC Batch function

        :param all_requests: (List) A list of gRPC AllRequest objects
        :param db_type: (str) The database type
        :return: (Response) The response object containing values corresponding to the request
        """
        meta = self._make_meta(db_type)
        batch_request = server_pb2.BatchRequest(meta=meta, batchrequest=all_requests)
        return Response(self.stub.Batch(batch_request))

    def profile(self, _id: str, db_type: str) -> Response:
        """
        Calls the gRPC Profile function

        :param _id: (str) The user's id
        :param db_type: (str) The database type
        :return: (Response) The response object containing values corresponding to the request
        """
        meta = self._make_meta(db_type=db_type)
        profile_request = server_pb2.ProfileRequest(id=_id, meta=meta)
        return Response(self.stub.Profile(profile_request))

    def profiles(self, db_type: str) -> Response:
        """
        Calls the gRPC Profiles function

        :param db_type: (str) The database type
        :return: (Response) The response object containing values corresponding to the request
        """
        meta = self._make_meta(db_type=db_type)
        profiles_request = server_pb2.ProfilesRequest(meta=meta)
        return Response(self.stub.Profiles(profiles_request))

    def edit_profile(self, _id: str, email: str, name: str, password: str, db_type: str) -> Response:
        """
        Calls the gRPC EditProfile function

        :param _id: (str) The user's id
        :param email: (str) The (optional) new email id
        :param name: (str) Then (optional) new name
        :param password: (str) The (optional) new password
        :param db_type: (str) The database type
        :return: (Response) The response object containing values corresponding to the request
        """
        meta = self._make_meta(db_type=db_type)
        edit_profile_request = server_pb2.EditProfileRequest(id=_id, meta=meta)
        if email is not None:
            edit_profile_request.email = email
        if name is not None:
            edit_profile_request.name = name
        if password is not None:
            edit_profile_request.password = password
        return Response(self.stub.EditProfile(edit_profile_request))

    def sign_in(self, email: str, password: str, db_type: str) -> Response:
        """
        Calls the gRPC SignIn function

        :param email: (str) The user's email id
        :param password: (str) The user's password
        :param db_type: (str) The database type
        :return: (Response) The response object containing values corresponding to the request
        """
        meta = self._make_meta(db_type=db_type)
        sign_in_request = server_pb2.SignInRequest(email=email, password=password, meta=meta)
        return Response(self.stub.SignIn(sign_in_request))

    def sign_up(self, email: str, name: str, password: str, role: str, db_type: str) -> Response:
        """
        Calls the gRPC SignIn function

        :param email: (str) The user's email id
        :param name: (str) The user's name
        :param password: (str) The user's password
        :param role: (str) The user's role
        :param db_type: (str) The database type
        :return: (Response) The response object containing values corresponding to the request
        """
        meta = self._make_meta(db_type=db_type)
        sign_up_request = server_pb2.SignUpRequest(email=email, name=name, password=password, role=role, meta=meta)
        return Response(self.stub.SignUp(sign_up_request))

    def create_folder(self, path: str, name: str) -> Response:
        """
        Calls the gRPC CreateFolder function

        :param path: (str) The location in which the folder is to be added
        :param name: (str) The name of the folder
        :return: (Response) The response object containing values corresponding to the request
        """
        meta = self._make_meta()
        create_folder_request = server_pb2.CreateFolderRequest(path=path, name=name, meta=meta)
        return Response(self.stub.CreateFolder(create_folder_request))

    def delete_file(self, path: str) -> Response:
        """
        Calls the gRPC DeleteFile function

        :param path: (str) The location of the file to be deleted
        :return: (Response) The response object containing values corresponding to the request
        """
        meta = self._make_meta()
        delete_file_request = server_pb2.DeleteFileRequest(path=path, meta=meta)
        return Response(self.stub.DeleteFile(delete_file_request))

    def list_files(self, path: str) -> Response:
        """
        Calls the gRPC ListFiles function

        :param path: (str) The path of the folder to be searched
        :return: (Response) The response object containing values corresponding to the request
        """
        meta = self._make_meta()
        list_files_request = server_pb2.ListFilesRequest(path=path, meta=meta)
        return Response(self.stub.ListFiles(list_files_request))

    def upload_file(self, path: str, name: str, stream: io.BufferedReader) -> Response:
        """
        Calls the gRPC UploadFile function

        :param path: (str) The location in which the file needs to be uploaded
        :param name: (str) The name of the file to be created
        :param stream: (io.BufferedReader) A BufferedReader to read from
        :return: (Response) The response object containing values corresponding to the request
        """
        meta = self._make_meta()

        def iterator():
            yield server_pb2.UploadFileRequest(path=path, name=name, meta=meta)
            for chunk in iter(lambda: stream.read(constants.PayloadSize), b''):
                yield server_pb2.UploadFileRequest(payload=chunk)

        return Response(self.stub.UploadFile(iterator()))

    def download_file(self, path: str, stream: io.BufferedWriter) -> Response:
        """
        Calls the gRPC DownloadFile function

        :param path: (str) The location of the file which needs to be downloaded
        :param stream: (io.BufferedWriter) A BufferedWriter to write to
        :return: (Response) The response object containing values corresponding to the request
        """
        meta = self._make_meta()
        download_file_request = server_pb2.DownloadFileRequest(path=path, meta=meta)
        for response in self.stub.DownloadFile(download_file_request):
            if response.status == 200:
                stream.write(response.payload)
            else:
                return Response(server_pb2.Response(status=response.status, error=response.error))
        return Response(server_pb2.Response(status=200))

    def pubsub_publish(self, subject: str, msg) -> Response:
        """
        Calls the gRPC PubsubPublish function

        :param subject: (str) The subject to publish to
        :param msg: The message to be published
        :return: (Response) The response object containing values corresponding to the request
        """
        msg = obj_to_utf8_bytes(msg)
        meta = self._make_meta()
        publish_request = server_pb2.PubsubPublishRequest(subject=subject, msg=msg, meta=meta)
        return Response(self.stub.PubsubPublish(publish_request))


__all__ = ["Transport", "make_read_options"]
