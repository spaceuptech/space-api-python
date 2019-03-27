from typing import Optional, Dict, Any
from space_api.utils import generate_find, AND
from space_api.transport import make_meta, read, make_read_options


class Get:
    """
    The SQL Get Interface
    ::
        from space_api import API, AND, OR, COND
        api = API("My-Project", "http://localhost:8080")
        db = api.my_sql() # For a MySQL interface
        response = db.get('posts').where(AND(COND('title', '==', 'Title1'))).all()

    :param project_id: (str) The project ID
    :param collection: (str) The collection name
    :param url: (str) The project URL
    :param db_type: (str) The database type
    :param token: (str) The (optional) JWT Token
    """
    def __init__(self, project_id: str, collection: str, url: str, db_type: str, token: Optional[str] = None):
        self.project_id = project_id
        self.collection = collection
        self.url = url
        self.db_type = db_type
        self.token = token
        self.params = {'find': {}, 'options': {}}
        self.meta = make_meta(self.project_id, self.db_type, self.collection, self.token)

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
            select = {'author':1, 'title':1}
            response = db.get('posts').select(select).all()

        :param select: (*) The conditions to find by
        """
        self.params['options']['select'] = select
        return self

    def sort(self, *array) -> 'Get':
        """
        Sets the fields to sort the results
        ::
            # The given query will sort results first by age (asc) then by age (desc)
            response = db.get('posts').sort('title', '-age').all()

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
            response = db.get('posts').skip(10).all()

        :param offset: (int) The number of records to skip
        """
        self.params['options']['skip'] = offset
        return self

    def limit(self, _limit: int) -> 'Get':
        """
        Sets the limit on number of records returned by the query
        ::
            # The given query will limit the result to 10 records
            response = db.get('posts').limit(10).all()

        :param _limit: (int) The maximum number of results returned
        :return:
        """
        self.params['options']['limit'] = _limit
        return self

    def one(self) -> Dict[str, Any]:
        """
        Gets a single record (If no record is returned, the status code is 400)
        ::
            response = db.get('posts').one()

        :return: (dict{str:Any})  The response dictionary
        """
        # Set a default limit if offset is specified and limit is not specified.
        if self.params['options'].get('skip') is not None and self.params['options'].get('limit') is None:
            self.params['options']['limit'] = 1

        options = self.params['options']
        read_options = make_read_options(select=options.get('select'), sort=options.get('sort'),
                                         skip=options.get('skip'), limit=options.get('limit'),
                                         distinct=options.get('distinct'))
        return read(self.url, find=self.params['find'], operation='one', options=read_options, meta=self.meta)

    def all(self) -> Dict[str, Any]:
        """
        Gets multiple records
        ::
            response = db.get('posts').all()

        :return: (dict{str:Any})  The response dictionary
        """
        # Set a default limit if offset is specified and limit is not specified.
        if self.params['options'].get('skip') is not None and self.params['options'].get('limit') is None:
            self.params['options']['limit'] = 20

        options = self.params['options']
        read_options = make_read_options(select=options.get('select'), sort=options.get('sort'),
                                         skip=options.get('skip'), limit=options.get('limit'),
                                         distinct=options.get('distinct'))
        return read(self.url, find=self.params['find'], operation='all', options=read_options, meta=self.meta)


__all__ = ['Get']
