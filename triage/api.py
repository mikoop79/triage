import zmq
import msgpack
from time import sleep

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.bind("tcp://0.0.0.0:5001")
socket.setsockopt(zmq.SUBSCRIBE, '')

unpacker = msgpack.Unpacker()
packer = msgpack.Packer()

while True:
    unpacker.feed(socket.recv())
    for msg in unpacker:
        if type(msg) == dict:
            print msg

