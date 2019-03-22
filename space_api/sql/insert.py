from typing import Optional
from space_api.transport import make_meta, create


class Insert:
    def __init__(self, project_id: str, collection: str, url: str, db_type: str, token: Optional[str] = None):
        self.project_id = project_id
        self.collection = collection
        self.url = url
        self.db_type = db_type
        self.token = token

    def one(self, record):
        meta = make_meta(self.project_id, self.db_type, self.collection, self.token)
        return create(self.url, document=record, operation='one', meta=meta)

    def all(self, records):
        meta = make_meta(self.project_id, self.db_type, self.collection, self.token)
        return create(self.url, document=records, operation='all', meta=meta)


__all__ = ['Insert']
