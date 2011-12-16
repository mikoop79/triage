import zmq
import msgpack
import mongoengine
from mongoengine.queryset import DoesNotExist
from models import ErrorInstance, Error
import sys

# config
ZMQ_URI = "tcp://0.0.0.0:5001"
MONGO_URI = "mongodb://lcawood.vm"
MONGO_DB = "logs"

# zero mq
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.bind(ZMQ_URI)
socket.setsockopt(zmq.SUBSCRIBE, '')

# mongo
mongoengine.connect('logs', host='lcawood.vm')

# messagepack
unpacker = msgpack.Unpacker()


def handle_msg(msg):
    new = ErrorInstance.from_raw(msg)
    try:
        error = Error.objects.get(hash=new.get_hash())
        error.update_from_instance(new)
    except DoesNotExist:
        error = Error.from_instance(new)
    error.save()
 

# serve!
while True:
    unpacker.feed(socket.recv())
    for msg in unpacker:
        if type(msg) == dict:
            try:
                handle_msg(msg)
            except Exception as a:
                print >> sys.stderr, a
