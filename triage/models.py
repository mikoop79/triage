import settings
from pyramid.security import authenticated_userid
from pymongo.objectid import ObjectId


class Model(object):
    def __init__(self, data):
        self.__dict__ = data

    def __repr__(self):
        return self.__dict__.__repr__()

    def save(self, collection):
        return collection.save(self.__dict__)


class Error(Model):

    def get_instances(self):
        return self.instances


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

    @classmethod
    def get_user_by(self, request, dict):
        return request.db['users'].find_one(dict)
