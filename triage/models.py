import settings
from pymongo.objectid import ObjectId
import re
import md5

from mongoengine import *


digit_re = re.compile('\d')
hex_re = re.compile('["\'\s][0-9a-f]+["\'\s]')


class User(Document):
    name = StringField()
    email = EmailField(required=True)



class Comment(EmbeddedDocument):
    content = StringField()
    author = ReferenceField(User)


class ErrorInstance(EmbeddedDocument):
    type = StringField(required=True)
    message = StringField(required=True)
    line = IntField()
    file = StringField()


class Error(Document):
    hash = StringField(required=True)
    message = StringField(required=True)
    type = StringField(required=True)
    timelatest = DateTimeField()
    timefirst = DateTimeField()
    count = IntField()
    claimedby = ReferenceField(User)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))
    instances = ListField(EmbeddedDocumentField(ErrorInstance))

    def add_instance(self, new):
        self.hash = new.hash
        self.message = new.message
        self.timelatest = new.timestamp
        self.count = self.count + 1
        try:
            self.instances.append(new)
        except AttributeError:
            self.instances = [new]







def error_hash(identity):
    hash = ''
    for key in identity:
        hash = hash + key + ":" + str(identity[key])
    
    return md5.new(hash).hexdigest()


"""
class ErrorInstance(Model):

    def project(self):
        return Project(self.data['application'])

    def get_aggregate_identity(self):
        return {
            'application': self.application,
            'language': self.language,
            'type': self.type,
            'message': digit_re.sub('', hex_re.sub('', self.message))
        }




class Project:
    @classmethod
    def from_error(cls, error):
        return cls(error['application'])

    def __init__(self, name):
        self.settings = settings.PROJECTS[name]

    def get_collection(self, db):
        return db[self.settings['collection']]

"""


