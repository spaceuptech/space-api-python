from typing import Optional
from space_api.transport import make_meta, create


class Insert:
    def __init__(self, project_id: str, collection: str, url: str, token: Optional[str] = None):
        self.project_id = project_id
        self.collection = collection
        self.url = url
        self.db_type = "mongo"
        self.token = token
        self.meta = make_meta(self.project_id, self.db_type, self.collection, self.token)

    def one(self, record):
        return create(self.url, document=record, operation='one', meta=self.meta)

    def all(self, records):
        return create(self.url, document=records, operation='all', meta=self.meta)


__all__ = ['Insert']
