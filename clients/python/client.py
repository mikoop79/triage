import zmq
import msgpack
from time import time


class ZeroMQMessagePackClient:

    unpacker = msgpack.Unpacker()
    packer = msgpack.Packer()
    context = zmq.Context()

    def __init__(self, server_uri):
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(server_uri)

    def pack(self, data):
        return self.packer.pack(data)

    def unpack(self, message):
        self.unpacker.feed(message)
        return self.unpacker.unpack()

    def send(self, data):
        self.socket.send(self.pack(data))
        return self.unpack(self.socket.recv())


class TriageClient (ZeroMQMessagePackClient):

    def log_error(self, error):
        return self.send({
            'error': error,
            'time': time()
        })
    
    def log_message(self, level, message):
        return self.send({
            'level': level,
            'message': message,
            'time': time()
        })


client = TriageClient("tcp://127.0.0.1:5000")

client.log_message('warn', 'This is a warning')
client.log_message('warn', 'This is a warning')
client.log_message('warn', 'This is a warning')
client.log_message('warn', 'This is a warning')
client.log_message('warn', 'This is a warning')

