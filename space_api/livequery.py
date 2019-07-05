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
        self.store = []
        self.collection = collection
        self.client = Client()
        self.find = {}
        self.skip_initial = False
        self.changes_only = False  # no cache
        self.async_result = None
        self.on_snapshot = None
        self.on_error = None
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

    def _snapshot_callback(self, rows: List[server_pb2.FeedData]):
        """
        A utility function to call the on_snapshot function

        :param rows: (List[server_pb2.FeedData]) The list of server_pb2.FeedData
        """
        if len(rows) == 0:
            return
        if self.changes_only:
            for feed_data in rows:
                if not (self.skip_initial and feed_data.type == constants.Initial):
                    if feed_data.type != constants.Delete:
                        self.on_snapshot([], feed_data.type, json.loads(feed_data.payload))
                    else:
                        if self.db_type == constants.Mongo:
                            self.on_snapshot([], feed_data.type, {"_id": feed_data.docId})
                        else:
                            self.on_snapshot([], feed_data.type, {"id": int(feed_data.docId)})
        else:
            for feed_data in rows:
                if feed_data.type == constants.Initial:
                    self.store.append(
                        {'id': feed_data.docId, 'time': feed_data.timeStamp, 'payload': feed_data.payload,
                         'is_deleted': False})
                if feed_data.type == constants.Insert or feed_data.type == constants.Update:
                    exists = False
                    for i in range(len(self.store)):
                        row = self.store[i]
                        if row['id'] == feed_data.docId:
                            exists = True
                            if row['time'] <= feed_data.timeStamp:
                                row['time'] = feed_data.timeStamp
                                row['payload'] = feed_data.payload
                                row['is_deleted'] = False
                        self.store[i] = row
                    if not exists:
                        self.store.append(
                            {'id': feed_data.docId, 'time': feed_data.timeStamp, 'payload': feed_data.payload,
                             'is_deleted': False})
                elif feed_data.type == constants.Delete:
                    for i in range(len(self.store)):
                        row = self.store[i]
                        if row['id'] == feed_data.docId and row['time'] <= feed_data.timeStamp:
                            row['time'] = feed_data.timeStamp
                            row['payload'] = {}
                            row['is_deleted'] = True
                        self.store[i] = row
            change_type = rows[0].type
            if change_type == constants.Initial:
                if not self.skip_initial:
                    self.on_snapshot([json.loads(row['payload']) for row in self.store if not row['is_deleted']],
                                     change_type, {})
            else:  # There is definitely only 1 row
                if change_type != constants.Delete:
                    self.on_snapshot([json.loads(row['payload']) for row in self.store if not row['is_deleted']],
                                     change_type, json.loads(rows[0].payload))
                else:
                    if self.db_type == constants.Mongo:
                        self.on_snapshot([json.loads(row['payload']) for row in self.store if not row['is_deleted']],
                                         change_type, {"_id": rows[0].docId})
                    else:
                        self.on_snapshot([json.loads(row['payload']) for row in self.store if not row['is_deleted']],
                                         change_type, {"id": int(rows[0].docId)})

    def _run_client(self, _id: str):
        responses = self.stub.RealTime(self.client)
        try:
            for response in responses:
                if response.id == _id:
                    if response.ack:
                        self._snapshot_callback(response.feedData)
                    else:
                        self.on_error(response.error)
                        self.unsubscribe()
                        return
        except grpc._channel._Rendezvous as e:
            a = str(e).index('details = "')
            self.on_error("Error:", str(e)[a + 11:str(e).index('"', a + 11)])
            self.unsubscribe()
            return

    def _send(self, payload: server_pb2.RealTimeRequest):
        return self.client.add_request(payload)

    def options(self, changes_only: bool = False) -> 'LiveQuery':
        """
        Provides additional options for the live query
        :param changes_only: (bool) (default False) Do not cache the documents. Whenever a change occurs,
        call 'on_snapshot' with that change
        :return:
        """
        self.changes_only = changes_only
        self.skip_initial = changes_only
        return self

    def subscribe(self, on_snapshot: Callable, on_error: Callable) -> Callable:
        """
        Subscribes to the particular LiveQuery instance

        :param on_snapshot: (Callable) The function to be called when new live data is encountered (takes in docs(List),
            type of change(String) and the changed doc(dict))
        :param on_error: (Callable) The function to be called when an error occurs (takes in an error(str))
        :return: (Callable) The unsubscribe function
        """
        self.on_snapshot = on_snapshot
        self.on_error = on_error

        self.async_result = self.run_pool.apply_async(self._run_client, (self.id,))
        options = obj_to_utf8_bytes({"skipInitial": self.skip_initial})
        self.pool.map(self._send, (
            server_pb2.RealTimeRequest(token=self.token, dbType=self.db_type, project=self.project_id,
                                       group=self.collection, options=options,
                                       type=constants.TypeRealtimeSubscribe, id=self.id,
                                       where=obj_to_utf8_bytes(self.find)),))
        return self.unsubscribe

    def unsubscribe(self):
        """
        Unsubscribes from the particular LiveQuery instance
        """
        options = obj_to_utf8_bytes({"skipInitial": self.skip_initial})
        self.pool.map(self._send, (
            server_pb2.RealTimeRequest(token=self.token, dbType=self.db_type, project=self.project_id,
                                       group=self.collection, options=options,
                                       type=constants.TypeRealtimeUnsubscribe, id=self.id,
                                       where=obj_to_utf8_bytes(self.find)),))
        self.client.close()
        self.run_pool.close()
        try:
            del self.store
        except KeyError:
            pass


__all__ = ['LiveQuery']
