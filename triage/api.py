import zmq
import msgpack
import mongoengine
import logging
from sys import argv
from pyramid.paster import get_appsettings
from models import Error

#logging
logging.basicConfig(level=logging.DEBUG)


# config
logging.info('Loading configuration')
ZMQ_URI = "tcp://0.0.0.0:5001"
settings = get_appsettings(argv[1], 'triage')

# zero mq
logging.info('Initializing zeromq socket at: ' + ZMQ_URI)
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.bind(ZMQ_URI)
socket.setsockopt(zmq.SUBSCRIBE, '')

# mongo
logging.info('Connecting to mongo at: mongodb://' + settings['mongodb.host'] + '/' + settings['mongodb.db_name'])
mongoengine.connect(settings['mongodb.db_name'], host=settings['mongodb.host'])

# messagepack
unpacker = msgpack.Unpacker()

# serve!
logging.info('Serving!')
while True:
    unpacker.feed(socket.recv())
    for msg in unpacker:
        if type(msg) == dict:
            try:
                error = Error.create_from_msg(msg)
                error.save()
            except Exception, a:
                logging.exception('Failed to process error')
