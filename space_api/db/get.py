from space_api.utils import generate_find, AND
from space_api.transport import Transport, make_read_options
from space_api.response import Response


class Get:
    """
    The DB Get Class
    ::
        from space_api import API, AND, OR, COND
        api = API("My-Project", "localhost:4124")
        db = api.mongo()
        response = db.get('posts').where(AND(COND('title', '==', 'Title1'))).apply()

    :param transport: (Transport) The API's transport instance
    :param collection: (str) The collection name
    :param db_type: (str) The database type
    :param operation: (str) The (optional) operation (one/all/distinct/count) (Defaults to 'all')
    """

    def __init__(self, transport: Transport, collection: str, db_type: str, operation: str = 'all'):
        self.transport = transport
        self.collection = collection
        self.db_type = db_type
        self.operation = operation
        self.params = {'find': {}, 'options': {}}

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
        """
        self.params['options']['limit'] = _limit
        return self

    def key(self, key) -> 'Get':
        """
        Sets the key for distinct values

        :param key: The key for distinct values
        """
        self.params['options']['distinct'] = key
        return self

    def apply(self) -> Response:
        """
        Triggers the get request
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
        return self.transport.read(self.params['find'], self.operation, read_options, self.db_type, self.collection)


__all__ = ['Get']
