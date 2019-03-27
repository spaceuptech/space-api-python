from typing import Optional, Dict, Any
from space_api.utils import generate_find, AND
from space_api.transport import make_meta, delete


class Delete:
    """
    The Mongo Delete Interface
    ::
        from space_api import API, AND, OR, COND
        api = API("My-Project", "http://localhost:8080")
        db = api.mongo()
        response = db.delete('posts').where(AND(COND('title', '==', 'Title1'))).all()

    :param project_id: (str) The project ID
    :param collection: (str) The collection name
    :param url: (str) The project URL
    :param token: (str) The (optional) JWT Token
    """
    def __init__(self, project_id: str, collection: str, url: str, token: Optional[str] = None):
        self.project_id = project_id
        self.collection = collection
        self.url = url
        self.db_type = "mongo"
        self.token = token
        self.params = {'find': {}}
        self.meta = make_meta(self.project_id, self.db_type, self.collection, self.token)

    def where(self, *conditions) -> 'Delete':
        """
        Prepares the find parameters

        :param conditions: (*) The conditions to find by
        """
        self.params['find'] = generate_find(AND(*conditions))
        return self

    def one(self) -> Dict[str, Any]:
        """
        Deletes one record, which matches first

        :return: (dict{str:Any})  The response dictionary
        """
        return delete(self.url, find=self.params['find'], operation='one', meta=self.meta)

    def all(self) -> Dict[str, Any]:
        """
        Deletes all matching records

        :return: (dict{str:Any})  The response dictionary
        """
        return delete(self.url, find=self.params['find'], operation='all', meta=self.meta)


__all__ = ['Delete']
