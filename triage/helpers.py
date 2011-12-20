from pymongo.code import Code
from pymongo import DESCENDING
from time import time
from models import Error, ErrorInstance

def handle_msg(msg):
    new = ErrorInstance.from_raw(msg)
    try:
        error = Error.objects.get(hash=new.get_hash())
        error.update_from_instance(new)
    except DoesNotExist:
        error = Error.from_instance(new)
    error.save()
