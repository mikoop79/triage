import settings
import re
import md5
from time import time
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


class ErrorInstance(EmbeddedDocument):
    project = StringField(required=True)
    language = StringField(required=True)
    type = StringField(required=True)
    message = StringField(required=True)
    timecreated = IntField()
    line = IntField()
    file = StringField()
    context = DictField()
    backtrace = ListField(DictField())

    @classmethod
    def from_raw(cls, raw):
        doc = cls(**raw)
        doc.timecreated = int(time())
        return doc

    def get_hash(self):
        return error_hash({
            'project': self.project,
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
    timelatest = IntField()
    timefirst = IntField()
    count = IntField()
    claimedby = ReferenceField(User)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))
    instances = ListField(EmbeddedDocumentField(ErrorInstance))
    seen = BooleanField()
    hidden = BooleanField()

    @classmethod
    def from_instance(cls, instance):
        error = cls()
        error.hash = instance.get_hash()
        error.project = instance.project
        error.language = instance.language
        error.type = instance.type
        error.timelatest = instance.timecreated
        error.timefirst = instance.timecreated
        error.message = instance.message
        error.count = 1
        error.instances = [instance]
        return error

    def update_from_instance(self, new):
        self.message = new.message
        self.timelatest = new.timecreated
        self.count = self.count + 1
        self.instances.append(new)




if __name__ == "__main__":
    from mongoengine.queryset import DoesNotExist

    connect('logs', host='lcawood.vm')

    new = ErrorInstance.from_raw({
        'project': 'test',
        'language': 'PHP',
        'type': 'TestingException',
        'message': 'Error on line 123',
        'line': 123,
        'file': 'testing.py',
        'context': { 'host': 'google.com' },
        'backtrace': [{ 'file': 'another.py', 'line': 45, 'function': 43}, { 'file': 'another.py', 'line': 45, 'function': 43}]
    })

    try:   
        error = Error.objects.get(hash=new.get_hash())
        error.update_from_instance(new)
    except DoesNotExist:
        error = Error.from_instance(new)
    error.save()    



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


