from typing import Optional, Dict, Any
from space_api.transport import make_meta, aggregate


class Aggregate:
    """
    The Mongo Aggregate Interface
    ::
        from space_api import API, AND, OR, COND
        api = API("My-Project", "http://localhost:8080")
        db = api.mongo()
        _pipe = [
            {'$match': {'status': 'A'}},
            {'$group': {'_id': '$cust_id', 'total': {'$sum': '$amount'}}}
        ]
        response = db.aggr('posts').pipe(_pipe).all()

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
        self.params = {}
        self.meta = make_meta(self.project_id, self.db_type, self.collection, self.token)

    def pipe(self, pipe_obj) -> 'Aggregate':
        """
        Prepares the pipe query

        :param pipe_obj: The pipeline object
        """
        self.params['pipe'] = pipe_obj
        return self

    def one(self) -> Dict[str, Any]:
        """
        Makes a query and returns a single object
        ::
            response = db.aggr('posts').pipe([...]).one()

        :return: (dict{str:Any})  The response dictionary
        """
        return aggregate(self.url, pipeline=self.params['pipe'], operation='one', meta=self.meta)

    def all(self) -> Dict[str, Any]:
        """
        Makes a query and returns all objects
        ::
            response = db.aggr('posts').pipe([...]).all()

        :return: (dict{str:Any})  The response dictionary
        """
        return aggregate(self.url, pipeline=self.params['pipe'], operation='all', meta=self.meta)


__all__ = ['Aggregate']
