from typing import Optional
from space_api.transport import make_meta, aggregate


class Aggregate:
    def __init__(self, project_id: str, collection: str, url: str, token: Optional[str] = None):
        self.project_id = project_id
        self.collection = collection
        self.url = url
        self.db_type = "mongo"
        self.token = token
        self.params = {}
        self.meta = make_meta(self.project_id, self.db_type, self.collection, self.token)

    def pipe(self, pipe_obj):
        self.params['pipe'] = pipe_obj
        return self

    def one(self):
        return aggregate(self.url, pipeline=self.params['pipe'], operation='one', meta=self.meta)

    def all(self):
        return aggregate(self.url, pipeline=self.params['pipe'], operation='all', meta=self.meta)


__all__ = ['Aggregate']
