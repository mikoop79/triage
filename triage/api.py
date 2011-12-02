import zmq
import msgpack
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://0.0.0.0:11300")

unpacker = msgpack.Unpacker()
packer = msgpack.Packer()

while True:
    try:
        unpacker.feed(socket.recv())
        msg = unpacker.unpack()
        socket.send(packer.pack({'status': 'ok'}))
        print msg

    except Exception as inst:
        print "Error" 
        print inst

