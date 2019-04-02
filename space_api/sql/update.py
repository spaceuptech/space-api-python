from typing import Optional, Dict, Any
from space_api.utils import generate_find, AND
from space_api.transport import make_meta, update


class Update:
    """
    The SQL Update Interface
    ::
        from space_api import API, AND, OR, COND
        api = API("My-Project", "http://localhost:8080")
        db = api.my_sql() # For a MySQL interface
        response = db.update('posts').where(AND(COND('title', '==', 'Title1'))).set({'title':'Title2'}).all()

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
        self.params = {'find': {}, 'update': {}}
        self.meta = make_meta(self.project_id, self.db_type, self.collection, self.token)

    def where(self, *conditions) -> 'Update':
        """
        Prepares the find parameters

        :param conditions: (*) The conditions to find by
        """
        self.params['find'] = generate_find(AND(*conditions))
        return self

    def set(self, obj) -> 'Update':
        """
        Prepares the updated values

        :param obj: The object containing the fields to set
        """
        self.params['update'] = {'$set': obj}
        return self

    def all(self) -> Dict[str, Any]:
        """
        Updates all matching records

        :return: (dict{str:Any})  The response dictionary
        """
        return update(self.url, find=self.params['find'], operation='all', _update=self.params['update'],
                      meta=self.meta)


__all__ = ['Update']
