import settings
from pyramid.security import authenticated_userid
from pymongo.objectid import ObjectId


class Model(object):

    def __init__(self, data):
        self.data = data

    def __get__(self, obj, cls=None):
        return self.data[obj]

    def __set__(self, obj, val):
        self.data[obj] = val
        return self.data[obj]

    def __delete__(self, obj):
        del self.data[obj]
        return self.data[obj]

    def save(self, collection):
        collection.save(self.data)


class Error(Model):
    pass


class ErrorInstance(Model):

    def project(self):
        return Project(self.data['application'])

    def get_aggregate_identity(self):
        return {
            'type': self.type,
            'line': self.line,
            'file': self.file,
        }


class Project:
    @classmethod
    def from_error(cls, error):
        return cls(error['application'])

    def __init__(self, name):
        self.settings = settings.PROJECTS[name]

    def get_collection(self, db):
        return db[self.settings['collection']]


class User(Model):

    @classmethod
    def get_user(self, request):
        userid = authenticated_userid(request)
        if not userid:
            return

        return request.db['users'].find_one({'_id': ObjectId(userid)})
