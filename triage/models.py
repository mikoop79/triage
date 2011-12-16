import settings
from pyramid.security import authenticated_userid
from pymongo.objectid import ObjectId


class Model(object):

    def __init__(self, data):
        self.data = data

    def __getattr__(self, name):
        return self.data[name]

    def __setattr__(self, name, val):
        self.data[name] = val
        return self.data[name]

    def __delattr__(self, name):
        del self.data[name]

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
