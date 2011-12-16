import zmq
import msgpack
import mongoengine
from time import sleep

from models import Project


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

# serve!
while True:
    unpacker.feed(socket.recv())
    for msg in unpacker:
        if type(msg) == dict:
            try:
                new = ErrorInstance(msg)

            except:
                print "Error"