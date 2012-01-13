import re
import md5
from time import time
from mongoengine import *
from mongoengine.queryset import DoesNotExist, QuerySet
from passlib.apps import custom_app_context as pwd_context

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

    @classmethod
    def from_data(cls, data):
        return cls(
                name=data['name'],
                email=data['email'],
                password=pwd_context.encrypt(data['password']),
                created=int(time())
            )


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


class ErrorQuerySet(QuerySet):
    def find_for_list(self, project, user, show):
        selected_project = project['id']
        if show == 'all':
            return self.filter(project=selected_project)
        elif show == 'hidden':
            return self.filter(project=selected_project, hidden=True)
        elif show == 'seen':
            return self.filter(project=selected_project, seen=True, hidden__ne=True)
        elif show == 'unseen':
            return self.filter(project=selected_project, seen__ne=True, hidden__ne=True)
        elif show == 'mine':
            return self.filter(project=selected_project, claimedby=user)
        elif show == 'unclaimed':
            return self.filter(project=selected_project, claimedby__exists=False)


class Error(Document):
    meta = {'queryset_class': ErrorQuerySet}

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
    def create_from_msg(cls, msg):
        new = ErrorInstance.from_raw(msg)
        try:
            error = cls.objects.get(hash=new.get_hash())
            error.update_from_instance(new)
        except DoesNotExist:
            error = cls.create_from_instance(new)
        return error

    @classmethod
    def create_from_instance(cls, instance):
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
