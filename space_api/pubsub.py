from typing import Callable
import uuid
from multiprocessing.pool import ThreadPool
import grpc
import json
from concurrent import futures
from space_api.proto import server_pb2
from space_api.response import Response
from space_api import constants
from space_api.utils import Client
from space_api.transport import Transport


class PubsubSubscription:
    """
    The PubsubSubscription Class

    :param subject: (str) The subject to which it is subscribed
    :param unsubscribe_func: (Callable) The unsubscribe function
    """
    def __init__(self, subject: str, unsubscribe_func: Callable):
        self.subject = subject
        self.unsubscribe_func = unsubscribe_func

    def unsubscribe(self):
        return self.unsubscribe_func(self.subject)


class Pubsub:
    """
    The Pubsub Class
    ::
        from space_api import API
        api = API('project', 'localhost:4124')
        pubsub = api.pubsub()

    :param transport: (Transport) The API's transport instance
    """

    def __init__(self, transport: Transport):
        self.transport = transport
        self.stub = transport.stub
        self.project_id = transport.project_id
        self.token = transport.token
        self.client = Client()
        self.async_result = None
        self.on_receive = None
        self.id = str(uuid.uuid1())
        self.pool = futures.ThreadPoolExecutor()
        self.run_pool = ThreadPool(processes=1)
        self.subscription = None
        # TODO Register Callbacks for Reconnect

    def _run_client(self, _id: str):
        responses = self.stub.PubsubSubscribe(self.client)
        try:
            for response in responses:
                if response.id == _id:
                    if response.type == constants.TypePubsubSubscribeFeed:
                        msg = json.loads(response.msg)
                        self.on_receive(msg['subject'], msg['data'])
                    elif response.status != 200:
                        print("Pubsub Error:", f"OperationType={response.type}", f"Status={response.status}",
                              response.error)
                        self.subscription.unsubscribe()
                        return
        except grpc._channel._Rendezvous as e:
            a = str(e).index('details = "')
            print("Transport Error:", str(e)[a + 11:str(e).index('"', a + 11)])
            self.subscription.unsubscribe()
            return

    def _send(self, payload: server_pb2.PubsubSubscribeRequest):
        return self.client.add_request(payload)

    def subscribe(self, subject: str, on_receive: Callable) -> PubsubSubscription:
        """
        Subscribes to the particular pubsub subject and its children

        :param subject: (str) The subject to subscribe to
        :param on_receive: (Callable) The function to be called when a message is published to the subject or to its children
        :return: (PubsubSubscription) The PubsubSubscription instance
        """
        return self.queue_subscribe(subject, "", on_receive)

    def queue_subscribe(self, subject: str, queue: str, on_receive: Callable) -> PubsubSubscription:
        """
        Subscribes to the particular pubsub subject and its children

        :param subject: (str) The subject to subscribe to
        :param queue: (str) The queue name
        :param on_receive: (Callable) The function to be called when a message is published to the subject or to its children
        :return: (PubsubSubscription) The PubsubSubscription instance
        """
        self.on_receive = on_receive
        self.async_result = self.run_pool.apply_async(self._run_client, (self.id,))
        self.pool.map(self._send, (
            server_pb2.PubsubSubscribeRequest(subject=subject, queue=queue, type=constants.TypePubsubSubscribe,
                                              token=self.token, project=self.project_id, id=self.id),))
        self.subscription = PubsubSubscription(subject, self._unsubscribe)
        return self.subscription

    def _unsubscribe(self, subject: str):
        """
        Unsubscribes from the particular subject and its children
        """
        self.pool.map(self._send, (
            server_pb2.PubsubSubscribeRequest(subject=subject, type=constants.TypePubsubUnsubscribe,
                                              token=self.token, project=self.project_id, id=self.id),))
        self.client.close()
        self.run_pool.close()

    def publish(self, subject: str, msg) -> Response:
        """
        Triggers the pubsub publish request

        :param subject: (str) The subject to publish to
        :param msg: The message to be published
        :return: (Response) The response object containing values corresponding to the request
        """
        return self.transport.pubsub_publish(subject, msg)


__all__ = ['Pubsub']
