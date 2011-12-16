import settings


class Model(object):

    def __init__(self, data):
        self.data = data

    def __get__(self, obj, cls=None):
        return self.data[obj]
    
    def __set__(self, obj, val):
        return (self.data[obj] = val)
    
    def __delete__(self, obj):
        return (del self.data[obj])

    def save(self, collection):
        collection.save(self.data)


class Error(Model):
    pass



class ErrorInstance(Model):
 
    def project(self):
        return Project(self.data['application'])

    def get_aggregate_identity():
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



class User(model):
    pass
