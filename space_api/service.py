import uuid
import json
import collections
import threading
import grpc
from concurrent import futures
from typing import Callable
from space_api.proto import server_pb2, server_pb2_grpc
from space_api import constants
from space_api.utils import obj_to_utf8_bytes


class _Client:
    def __init__(self):
        self._stop_event = threading.Event()
        self._request_condition = threading.Condition()
        self._requests = collections.deque()

    def __next__(self):
        with self._request_condition:
            while (not self._requests and not self._stop_event.is_set()) or len(self._requests) <= 0:
                self._request_condition.wait()
            if len(self._requests) > 0:
                return self._requests.popleft()

    def close(self):
        self._stop_event.set()
        with self._request_condition:
            self._request_condition.notify()

    def add_request(self, request):
        with self._request_condition:
            self._requests.append(request)
            self._request_condition.notify()


class Service:
    """
    The Service Interface
    ::
        from space_api import API
        api = API('project', 'localhost:8081')

        service = api.service('service')
        service.register_function(my_awesome_function)
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
        self.client = _Client()
        self.uid = str(uuid.uuid1())
        self.pool = futures.ThreadPoolExecutor()

    def register_function(self, func_name: str, function: Callable):
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
            a = str(e).index('details = "')
            raise Exception(str(e)[a + 11:str(e).index('"', a + 11)])

    def start(self):
        """
        Start the Service (Blocking)
        """
        client_thread = threading.Thread(target=self._run_client)
        client_thread.start()

        self.pool.map(self._func, (server_pb2.FunctionsPayload(service=self.service, type=constants.TypeServiceRegister,
                                                               id=self.uid, project=self.project_id,
                                                               token=self.token),))

        self.client.close()
        client_thread.join()


__all__ = ['Service']
