import uuid
import json
import collections
import threading
import grpc
from concurrent import futures
from typing import Optional, Callable
from space_api.proto import server_pb2, server_pb2_grpc
from space_api import constants
from space_api.utils import obj_to_utf8_bytes


class Client:
    def __init__(self):
        self._stop_event = threading.Event()
        self._request_condition = threading.Condition()
        self._requests = collections.deque()
        self._responses = {}

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
    def __init__(self, stub: server_pb2_grpc.SpaceCloudStub, project_id: str, token: str, service: str):
        self.stub = stub
        self.project_id = project_id
        self.token = token
        self.service = service
        self.storage = {}
        self.client = Client()
        self.uid = str(uuid.uuid1())
        self.pool = futures.ThreadPoolExecutor(max_workers=8)

    def register_function(self, function: Callable, func_name: Optional[str] = None):
        if func_name is not None:
            self.storage[func_name] = function
        else:
            self.storage[function.__name__] = function

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
                            result = self.storage[response.function](json.loads(response.params),
                                                                     json.loads(response.auth))
                            payload = server_pb2.FunctionsPayload(id=response.id, type=constants.TypeServiceRequest,
                                                                  service=self.service,
                                                                  params=obj_to_utf8_bytes(result))
                        except Exception as e:
                            payload = server_pb2.FunctionsPayload(id=response.id, type=constants.TypeServiceRequest,
                                                                  service=self.service, error=str(e))
                    else:
                        payload = server_pb2.FunctionsPayload(id=response.id, type=constants.TypeServiceRequest,
                                                              service=self.service, error="Function not registered")
                    self.pool.map(self._func, (payload,))
        except grpc._channel._Rendezvous as e:
            a = str(e).index('details = "')
            raise Exception(str(e)[a + 11:str(e).index('"', a + 11)])

    def start(self):
        client_thread = threading.Thread(target=self._run_client)
        client_thread.start()

        self.pool.map(self._func, (server_pb2.FunctionsPayload(service=self.service, type=constants.TypeServiceRegister,
                                                               id=self.uid, project=self.project_id,
                                                               token=self.token),))

        self.client.close()
        client_thread.join()


__all__ = ['Service']
