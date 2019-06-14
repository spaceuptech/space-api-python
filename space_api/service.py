import uuid
import json
import grpc
from concurrent import futures
from multiprocessing.pool import ThreadPool
from typing import Callable
from space_api.proto import server_pb2, server_pb2_grpc
from space_api import constants
from space_api.utils import obj_to_utf8_bytes, Client


class Service:
    """
    The Service Class
    ::
        from space_api import API
        api = API('project', 'localhost:8081')

        service = api.service('service')
        service.register_func(my_awesome_function)
        service.start()
        api.close()

    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param project_id: (str) The project ID
    :param token: (str) The (optional) JWT Token
    :param service: (str) The name of the Service
    """

    def __init__(self, stub: server_pb2_grpc.SpaceCloudStub, project_id: str, token: str, service: str):
        self.stub = stub
        self.project_id = project_id
        self.token = token
        self.service = service
        self.storage = {}
        self.client = Client()
        self.uid = str(uuid.uuid1())
        self.pool = futures.ThreadPoolExecutor()

    def register_func(self, func_name: str, function: Callable):
        """
        Register a function with the Service

        :param function: The function to register
        :param func_name: (str) The name with which the function should be called
        """
        self.storage[func_name] = function

    def _func(self, payload):
        return self.client.add_request(payload)

    def _run_client(self):
        responses = self.stub.Service(self.client)
        try:
            for response in responses:
                if response.type == constants.TypeServiceRegister:
                    if response.id == self.uid:
                        if len(response.params) > 0:
                            if json.loads(response.params).get('ack'):
                                print("Registered Service:", self.service)
                if response.type == constants.TypeServiceRequest:
                    if response.function in self.storage:
                        try:
                            def callback(kind: str, result):
                                if kind == "response":
                                    self.pool.map(self._func, (
                                        server_pb2.FunctionsPayload(id=response.id, type=constants.TypeServiceRequest,
                                                                    service=self.service,
                                                                    params=obj_to_utf8_bytes(result)),))
                                else:
                                    raise ValueError("The kind (1st parameter) should be 'response'")

                            self.storage[response.function](json.loads(response.params), json.loads(response.auth),
                                                            callback)
                        except ValueError as e:
                            if str(e) == "The kind (1st parameter) should be 'response'":
                                raise e
                            else:
                                self.pool.map(self._func, (
                                    server_pb2.FunctionsPayload(id=response.id, type=constants.TypeServiceRequest,
                                                                service=self.service, error=str(e)),))
                        except Exception as e:
                            self.pool.map(self._func, (
                                server_pb2.FunctionsPayload(id=response.id, type=constants.TypeServiceRequest,
                                                            service=self.service, error=str(e)),))
                    else:
                        self.pool.map(self._func,
                                      (server_pb2.FunctionsPayload(id=response.id, type=constants.TypeServiceRequest,
                                                                   service=self.service,
                                                                   error="Function not registered"),))
        except grpc._channel._Rendezvous as e:
            raise e
            # a = str(e).index('details = "')
            # print("Error:", str(e)[a + 11:str(e).index('"', a + 11)])
            # raise Exception(str(e)[a + 11:str(e).index('"', a + 11)])
        return None

    def start(self):
        """
        Start the Service (Blocking)
        """
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(self._run_client, ())
        self.pool.map(self._func, (server_pb2.FunctionsPayload(service=self.service, type=constants.TypeServiceRegister,
                                                               id=self.uid, project=self.project_id,
                                                               token=self.token),))

        self.client.close()
        err = async_result.get()
        print(err)


__all__ = ['Service']
