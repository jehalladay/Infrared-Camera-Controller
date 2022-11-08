import zmq
import time

context = zmq.Context()

messager = context.socket(zmq.REQ)
messager.connect("tcp://localhost:4999")

for i in range (10):
    messager.send(b"Hello\n")
    time.sleep(10)
