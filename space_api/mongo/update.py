from typing import Optional
from space_api.utils import generate_find, AND
from space_api.transport import make_meta, update


class Update:
    def __init__(self, project_id: str, collection: str, url: str, token: Optional[str] = None):
        self.project_id = project_id
        self.collection = collection
        self.url = url
        self.db_type = "mongo"
        self.token = token
        self.params = {'find': {}, 'update': {'$set': {}}}
        self.meta = make_meta(self.project_id, self.db_type, self.collection, self.token)

    def where(self, *conditions):
        self.params['find'] = generate_find(AND(*conditions))
        return self

    def set(self, obj):
        self.params['update']['$set'] = obj
        return self

    def push(self, obj):
        self.params['update']['$push'] = obj
        return self

    def remove(self, *fields):
        self.params['update']['$unset'] = {x: '' for x in fields}
        return self

    def rename(self, obj):
        self.params['update']['$rename'] = obj
        return self

    def inc(self, obj):
        self.params['update']['$inc'] = obj
        return self

    def mul(self, obj):
        self.params['update']['$mul'] = obj
        return self

    def max(self, obj):
        self.params['update']['$max'] = obj
        return self

    def min(self, obj):
        self.params['update']['$min'] = obj
        return self

    def current_timestamp(self, *values):
        if self.params['update'].get('$currentDate') is None:
            self.params['update']['$currentDate'] = {}
        self.params['update']['$currentDate'].update({x: {'$type': 'timestamp'} for x in values})
        return self

    def current_date(self, *values):
        if self.params['update'].get('$currentDate') is None:
            self.params['update']['$currentDate'] = {}
        self.params['update']['$currentDate'].update({x: {'$type': 'date'} for x in values})
        return self

    def one(self):
        return update(self.url, find=self.params['find'], operation='one', _update=self.params['update'],
                      meta=self.meta)

    def all(self):
        return update(self.url, find=self.params['find'], operation='all', _update=self.params['update'],
                      meta=self.meta)

    def upsert(self):
        return update(self.url, find=self.params['find'], operation='upsert', _update=self.params['update'],
                      meta=self.meta)


__all__ = ['Update']
