from typing import Optional
from space_api.transport import make_meta, create


class Insert:
    """
    The SQL Insert Interface
    ::
        from space_api import API
        api = API("My-Project", "http://localhost:8080")
        db = api.my_sql() # For a MySQL interface
        record = {'author': 'John', 'title': 'Title1'}
        response = db.insert('posts').one(record)

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
        self.meta = make_meta(self.project_id, self.db_type, self.collection, self.token)

    def one(self, record):
        """
        Inserts a single record
        ::
            record = {'author': 'John', 'title': 'Title1'}
            response = db.insert('posts').one(record)

        :param record: The record to insert
        :return: (dict{str:Any}) The response dictionary
        """
        return create(self.url, document=record, operation='one', meta=self.meta)

    def all(self, records):
        """
        Inserts multiple records
        ::
            records = [{'author': 'John', 'title': 'Title1'}]
            response = db.insert('posts').all(records)

        :param records: (list) The records to insert
        :return: (dict{str:Any}) The response dictionary
        """
        return create(self.url, document=records, operation='all', meta=self.meta)


__all__ = ['Insert']
