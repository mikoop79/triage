import settings
import re
import md5

from mongoengine import *


digit_re = re.compile('\d')
hex_re = re.compile('["\'\s][0-9a-f]+["\'\s]')

def error_hash(identity):
    hash = ''
    for key in identity:
        hash = hash + key + ":" + str(identity[key])
    
    return md5.new(hash).hexdigest()


class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True)
    password = StringField(required=True)
    created = IntField(required=True)


class Comment(EmbeddedDocument):
    author = ReferenceField(User, required=True)
    content = StringField(required=True)
    created = IntField(required=True)


class BackTraceEntry(EmbeddedDocument):
    file = StringField()
    line = IntField()
    function = StringField()


class ErrorInstance(EmbeddedDocument):
    project = StringField(required=True)
    language = StringField(required=True)    
    type = StringField(required=True)
    message = StringField(required=True)
    timecreated = DateTimeField()
    line = IntField()
    file = StringField()
    context = DictField()
    backtrace = ListField(EmbeddedDocumentField(BackTraceEntry))

    @classmethod
    def from_raw(cls, raw):
        doc = cls(raw)
        doc.hash = doc.get_hash()

    def get_hash():
        return error_hash({
            'application': self.application,
            'language': self.language,
            'type': self.type,
            'message': digit_re.sub('', hex_re.sub('', self.message))
        })



class Error(Document):
    hash = StringField(required=True)
    project = StringField(required=True)
    language = StringField(required=True)
    message = StringField(required=True)
    type = StringField(required=True)
    timelatest = DateTimeField()
    timefirst = DateTimeField()
    count = IntField()
    claimedby = ReferenceField(User)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))
    instances = ListField(EmbeddedDocumentField(ErrorInstance))

    @classmethod
    def from_instance(instance):
        error = cls()
        error.hash = instance.hash
        error.project = instance.project
        error.language = instance.language
        error.type = instance.type
        error.timelatest = instance.timecreated
        error.timefirst = instance.timecreated
        error.count = 1
        error.instances = [instance]
        return error

    def update_from_instance(self, new):
        self.message = new.message
        self.timelatest = new.timestamp
        self.count = self.count + 1
        self.instances.append(new)






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


