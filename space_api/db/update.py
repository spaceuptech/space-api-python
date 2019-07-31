from space_api.utils import generate_find, AND
from space_api.transport import Transport
from space_api.response import Response


class Update:
    """
    The DB Update Class
    ::
        from space_api import API, AND, OR, COND
        api = API("My-Project", "localhost:4124")
        db = api.mongo()  # For a MongoDB interface
        response = db.update('posts').where(AND(COND('title', '==', 'Title1'))).set({'title':'Title2'}).apply()

    :param transport: (Transport) The API's transport instance
    :param collection: (str) The collection name
    :param db_type: (str) The database type
    :param operation: (str) The (optional) operation (one/all/upsert) (Defaults to 'all')
    """

    def __init__(self, transport: Transport, collection: str, db_type: str, operation: str = 'all'):
        self.transport = transport
        self.collection = collection
        self.db_type = db_type
        self.operation = operation
        self.params = {'find': {}, 'update': {}}

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
        ::
            response = db.update('posts').set({'author': 'Drake'}).apply()

        :param obj: An object containing the fields to set
        """
        self.params['update']['$set'] = obj
        return self

    def push(self, obj) -> 'Update':
        """
        Adds an item to an list
        ::
            response = db.update('posts').push({'author': 'Drake'}).apply()

        :param obj: An object containing the fields to set
        """
        self.params['update']['$push'] = obj
        return self

    def remove(self, *fields) -> 'Update':
        """
        Removes the specified fields from a document
        ::
            response = db.update('posts').remove('age', 'likes').apply()

        :param fields: (*) The fields to be removed
        """
        self.params['update']['$unset'] = {x: '' for x in fields}
        return self

    def rename(self, obj) -> 'Update':
        """
        Renames the specified fields
        ::
            response = db.update('posts').rename({'mobile': 'contact'}).apply()

        :param obj: An object containing the fields to rename
        """
        self.params['update']['$rename'] = obj
        return self

    def inc(self, obj) -> 'Update':
        """
        Increments the value of a field by a specified amount
        ::
            response = db.update('posts').inc({'views': 1}).apply()

        :param obj: An object containing the fields to increment, along with the increment value
        """
        self.params['update']['$inc'] = obj
        return self

    def mul(self, obj) -> 'Update':
        """
        Multiplies the value of a field by a specified amount
        ::
            response = db.update('posts').mul({'amount': 4}).apply()

        :param obj: An object containing the fields to multiply, along with the multiplier value
        """
        self.params['update']['$mul'] = obj
        return self

    def max(self, obj) -> 'Update':
        """
        Updates the field if the specified value is greater than the existing field value
        ::
            response = db.update('posts').max({'highScore': 1200}).apply()

        :param obj: An object containing the fields to set
        """
        self.params['update']['$max'] = obj
        return self

    def min(self, obj) -> 'Update':
        """
        Updates the field if the specified value is lesser than the existing field value
        ::
            response = db.update('posts').min({'lowestScore': 300}).apply()

        :param obj: An object containing the fields to set
        """
        self.params['update']['$min'] = obj
        return self

    def current_timestamp(self, *values) -> 'Update':
        """
        Sets the value of a field(s) to the current timestamp
        ::
            response = db.update('posts').current_timestamp('lastModified').apply()

        :param values: (*) A list containing the fields to set
        """
        if self.params['update'].get('$currentDate') is None:
            self.params['update']['$currentDate'] = {}
        self.params['update']['$currentDate'].update({x: {'$type': 'timestamp'} for x in values})
        return self

    def current_date(self, *values) -> 'Update':
        """
        Sets the value of a field(s) to the date
        ::
            response = db.update('posts').current_date('lastModified').apply()

        :param values: (*) A list containing the fields to set
        """
        if self.params['update'].get('$currentDate') is None:
            self.params['update']['$currentDate'] = {}
        self.params['update']['$currentDate'].update({x: {'$type': 'date'} for x in values})
        return self

    def apply(self) -> Response:
        """
        Triggers the update request

        :return: (Response) The response object containing values corresponding to the request
        """
        return self.transport.update(self.params['find'], self.operation, self.params['update'], self.db_type,
                                     self.collection)


__all__ = ['Update']
