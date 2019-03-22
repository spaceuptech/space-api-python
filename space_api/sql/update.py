from typing import Optional
from space_api.utils import generate_find, AND
from space_api.transport import make_meta, update


class Update:
    def __init__(self, project_id: str, collection: str, url: str, db_type: str, token: Optional[str] = None):
        self.project_id = project_id
        self.collection = collection
        self.url = url
        self.db_type = db_type
        self.token = token
        self.params = {'find': {}, 'update': {'$set': {}}}

    def where(self, *conditions):
        self.params['find'] = generate_find(AND(*conditions))
        return self

    def set(self, obj):
        self.params['update']['$set'] = obj
        return self

    def all(self):
        meta = make_meta(self.project_id, self.db_type, self.collection, self.token)
        return update(self.url, find=self.params['find'], operation='all', _update=self.params['update'], meta=meta)


__all__ = ['Update']
