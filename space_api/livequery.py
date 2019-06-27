from typing import Callable
import uuid
from multiprocessing.pool import ThreadPool
import grpc
import json
from concurrent import futures
from typing import List
from space_api.utils import generate_find, AND
from space_api.proto import server_pb2
from space_api import constants
from space_api.utils import Client, obj_to_utf8_bytes
from space_api.transport import Transport


def _snapshot_callback(storage: dict, rows: List[server_pb2.FeedData]):
    """
    A utility function to call the on_snapshot function

    :param storage: (dict) The LiveQuery storage
    :param rows: (List[server_pb2.FeedData]) The list of server_pb2.FeedData
    """
    if len(rows) == 0:
        return
    obj = {}
    for feedData in rows:
        # print(feedData)
        obj = storage[feedData.queryId]
        if feedData.type == constants.Insert or feedData.type == constants.Update:
            exists = False
            for i in range(len(obj['snapshot'])):
                row = obj['snapshot'][i]
                if row['id'] == feedData.docId:
                    exists = True
                    if row['time'] <= feedData.timeStamp:
                        row['time'] = feedData.timeStamp
                        row['payload'] = feedData.payload
                        row['is_deleted'] = False
                obj['snapshot'][i] = row
            if not exists:
                obj['snapshot'].append(
                    {'id': feedData.docId, 'time': feedData.timeStamp, 'payload': feedData.payload,
                     'is_deleted': False})
        elif feedData.type == constants.Delete:
            for i in range(len(obj['snapshot'])):
                row = obj['snapshot'][i]
                if row['id'] == feedData.docId and row['time'] <= feedData.timeStamp:
                    row['time'] = feedData.timeStamp
                    row['payload'] = {}
                    row['is_deleted'] = True
                obj['snapshot'][i] = row
    change_type = rows[0].type if len(rows) == 1 else 'initial'
    obj['subscription']['on_snapshot']([json.loads(row['payload']) for row in obj['snapshot'] if not row['is_deleted']],
                                       change_type)


class LiveQuery:
    """
    The LiveQuery Class
    ::
        from space_api import API
        api = API('project', 'localhost:8081')
        db = api.my_sql()

        unsubscribe = db.live_query('books').subscribe(on_snapshot, on_error)

        # After some condition
        unsubscribe()
        api.close()

    :param transport: (Transport) The API's transport instance
    :param db_type: (str) The database type
    :param collection: (str) The collection name
    """

    def __init__(self, transport: Transport, db_type: str, collection: str):
        self.stub = transport.stub
        self.project_id = transport.project_id
        self.token = transport.token
        self.db_type = db_type
        self.store = {}
        self.collection = collection
        self.client = Client()
        self.find = {}
        self.async_result = None
        self.id = str(uuid.uuid1())
        self.pool = futures.ThreadPoolExecutor()
        self.run_pool = ThreadPool(processes=1)
        # TODO Register Callbacks for Reconnect

    def where(self, *conditions) -> 'LiveQuery':
        """
        Prepares the find parameters

        :param conditions: (*) The conditions to find by
        """
        self.find = generate_find(AND(*conditions))
        return self

    def _run_client(self, _id: str, on_snapshot: Callable, on_error: Callable):
        responses = self.stub.RealTime(self.client)
        try:
            for response in responses:
                if response.id == _id:
                    if response.ack:
                        _snapshot_callback(self.store, response.feedData)
                    else:
                        on_error(response.error)
                        self.unsubscribe()
                        return
        except grpc._channel._Rendezvous as e:
            a = str(e).index('details = "')
            on_error("Error:", str(e)[a + 11:str(e).index('"', a + 11)])
            self.unsubscribe()
            return

    def _send(self, payload: server_pb2.RealTimeRequest):
        return self.client.add_request(payload)

    def subscribe(self, on_snapshot: Callable, on_error: Callable) -> Callable:
        """
        Subscribes to the particular LiveQuery instance

        :param on_snapshot: (Callable) The function to be called when new live data is encountered (takes in docs(List)
            and type of change(String))
        :param on_error: (Callable) The function to be called when an error occurs (takes in an error(str))
        :return: (Callable) The unsubscribe function
        """
        self.store[self.id] = {'snapshot': [], 'subscription': {}, 'find': self.find}
        subscription = {'on_snapshot': on_snapshot, 'on_error': on_error}
        self.store[self.id]['subscription'] = subscription

        self.async_result = self.run_pool.apply_async(self._run_client, (self.id, on_snapshot, on_error))
        self.pool.map(self._send, (
            server_pb2.RealTimeRequest(token=self.token, dbType=self.db_type, project=self.project_id,
                                       group=self.collection,
                                       type=constants.TypeRealtimeSubscribe, id=self.id,
                                       where=obj_to_utf8_bytes(self.find)),))
        return self.unsubscribe

    def unsubscribe(self):
        """
        Unsubscribes from the particular LiveQuery instance
        """
        self.pool.map(self._send, (
            server_pb2.RealTimeRequest(token=self.token, dbType=self.db_type, project=self.project_id,
                                       group=self.collection,
                                       type=constants.TypeRealtimeUnsubscribe, id=self.id,
                                       where=obj_to_utf8_bytes(self.find)),))
        self.client.close()
        self.run_pool.close()
        try:
            del self.store[self.id]
        except KeyError:
            pass


__all__ = ['LiveQuery']
