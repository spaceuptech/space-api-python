from typing import Optional
from space_api.utils import generate_find, AND
from space_api.transport import make_meta, read, make_read_options


class Get:
    def __init__(self, project_id: str, collection: str, url: str, token: Optional[str] = None):
        self.project_id = project_id
        self.collection = collection
        self.url = url
        self.db_type = "mongo"
        self.token = token
        self.params = {'find': {}, 'options': {}}
        self.meta = make_meta(self.project_id, self.db_type, self.collection, self.token)

    def where(self, *conditions):
        self.params['find'] = generate_find(AND(*conditions))
        return self

    def select(self, select):
        self.params['options']['select'] = select
        return self

    def sort(self, *array):
        ans = {}
        for val in array:
            if val.startswith("-"):
                ans[val[1:]] = -1
            else:
                ans[val] = 1
        self.params['options']['sort'] = ans
        return self

    def skip(self, offset: int):
        self.params['options']['skip'] = offset
        return self

    def limit(self, _limit: int):
        self.params['options']['limit'] = _limit
        return self

    def one(self):
        options = self.params['options']
        read_options = make_read_options(select=options.get('select'), sort=options.get('sort'),
                                         skip=options.get('skip'), limit=options.get('limit'),
                                         distinct=options.get('distinct'))
        return read(self.url, find=self.params['find'], operation='one', options=read_options, meta=self.meta)

    def all(self):
        # Set a default limit if offset is specified and limit is not specified.
        if self.params['options'].get('skip') is not None and self.params['options'].get('limit') is None:
            self.params['options']['limit'] = 20

        options = self.params['options']
        read_options = make_read_options(select=options.get('select'), sort=options.get('sort'),
                                         skip=options.get('skip'), limit=options.get('limit'),
                                         distinct=options.get('distinct'))
        return read(self.url, find=self.params['find'], operation='all', options=read_options, meta=self.meta)

    def distinct(self, key):
        self.params['options']['distinct'] = key
        options = self.params['options']
        read_options = make_read_options(select=options.get('select'), sort=options.get('sort'),
                                         skip=options.get('skip'), limit=options.get('limit'),
                                         distinct=options.get('distinct'))
        return read(self.url, find=self.params['find'], operation='distinct', options=read_options, meta=self.meta)

    def count(self):
        options = self.params['options']
        read_options = make_read_options(select=options.get('select'), sort=options.get('sort'),
                                         skip=options.get('skip'), limit=options.get('limit'),
                                         distinct=options.get('distinct'))
        return read(self.url, find=self.params['find'], operation='count', options=read_options, meta=self.meta)


__all__ = ['Get']
