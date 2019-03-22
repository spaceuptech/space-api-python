from typing import Optional
from space_api.utils import generate_find, AND
from space_api.transport import make_meta, delete


class Delete:
    def __init__(self, project_id: str, collection: str, url: str, db_type: str, token: Optional[str] = None):
        self.project_id = project_id
        self.collection = collection
        self.url = url
        self.db_type = db_type
        self.token = token
        self.params = {'find': {}}

    def where(self, *conditions):
        self.params['find'] = generate_find(AND(*conditions))
        return self

    def all(self):
        meta = make_meta(self.project_id, self.db_type, self.collection, self.token)
        return delete(self.url, find=self.params['find'], operation='all', meta=meta)


__all__ = ['Delete']
