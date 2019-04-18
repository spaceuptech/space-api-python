from typing import Optional
from space_api.utils import generate_find, AND
from space_api.transport import make_meta, read, make_read_options
from space_api.proto.server_pb2_grpc import SpaceCloudStub
from space_api.response import Response


class Get:
    """
    The SQL Get Interface
    ::
        from space_api import API, AND, OR, COND
        api = API("My-Project", "localhost:8080")
        db = api.my_sql() # For a MySQL interface
        response = db.get('posts').where(AND(COND('title', '==', 'Title1'))).apply()

    :param project_id: (str) The project ID
    :param collection: (str) The collection name
    :param stub: (server_pb2_grpc.SpaceCloudStub) The gRPC endpoint stub
    :param db_type: (str) The database type
    :param token: (str) The (optional) JWT Token
    :param operation: (str) The (optional) operation (one/all) (Defaults to 'all')
    """

    def __init__(self, project_id: str, collection: str, stub: SpaceCloudStub, db_type: str,
                 token: Optional[str] = None, operation: str = 'all'):
        self.project_id = project_id
        self.collection = collection
        self.stub = stub
        self.db_type = db_type
        self.token = token
        self.params = {'find': {}, 'options': {}}
        self.meta = make_meta(self.project_id, self.db_type, self.collection, self.token)
        self.operation = operation

    def where(self, *conditions) -> 'Get':
        """
        Prepares the find parameters

        :param conditions: (*) The conditions to find by
        """
        self.params['find'] = generate_find(AND(*conditions))
        return self

    def select(self, select) -> 'Get':
        """
        Sets the fields to be selected
        ::
            # Given query will only select author and title fields
            select = {'author':1, 'title':1}
            response = db.get('posts').select(select).apply()

        :param select: (*) The conditions to find by
        """
        self.params['options']['select'] = select
        return self

    def sort(self, *array) -> 'Get':
        """
        Sets the fields to sort the results
        ::
            # The given query will sort results first by age (asc) then by age (desc)
            response = db.get('posts').sort('title', '-age').apply()

        :param array: (*) The fields to sort the results by
        """
        ans = {}
        for val in array:
            if val.startswith("-"):
                ans[val[1:]] = -1
            else:
                ans[val] = 1
        self.params['options']['sort'] = ans
        return self

    def skip(self, offset: int) -> 'Get':
        """
        Sets the number of records to skip
        ::
            The given query will skip the first 10 records
            response = db.get('posts').skip(10).apply()

        :param offset: (int) The number of records to skip
        """
        self.params['options']['skip'] = offset
        return self

    def limit(self, _limit: int) -> 'Get':
        """
        Sets the limit on number of records returned by the query
        ::
            # The given query will limit the result to 10 records
            response = db.get('posts').limit(10).apply()

        :param _limit: (int) The maximum number of results returned
        :return:
        """
        self.params['options']['limit'] = _limit
        return self

    def apply(self) -> Response:
        """
        Triggers the get query
        ::
            response = db.get('posts').apply()

        :return: (Response) The response object containing values corresponding to the request
        """
        # Set a default limit if offset is specified and limit is not specified.
        if self.params['options'].get('skip') is not None and self.params['options'].get('limit') is None:
            self.params['options']['limit'] = 20

        options = self.params['options']
        read_options = make_read_options(select=options.get('select'), sort=options.get('sort'),
                                         skip=options.get('skip'), limit=options.get('limit'),
                                         distinct=options.get('distinct'))
        return read(self.stub, find=self.params['find'], operation=self.operation, options=read_options, meta=self.meta)


__all__ = ['Get']
