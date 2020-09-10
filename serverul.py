import threading
from threading import Thread
from multiprocessing import Queue
from queue import Queue
import sys
import socket
import select
import os
import time


class server(Thread):
    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(0)
        server.bind(("localhost", 50000))
        server.listen(1)
        inputs = [server]
        outputs = []
        message_queues = {}

        while inputs:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            for s in readable:
                if s in server:
                    connection, client_address = s.accept()
                    connection.setblocking(0)
                    inputs.append(connection)
                    message_queues[connection] = Queue.Queue()
                else:
                    data = s.recv(1024)
                    if data:
                        message_queues[s].put(data)
                        if s not in outputs:
                            outputs.append(s)
                    else:
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()
                        del message_queues[s]
            for s in writable:
                try:
                    next_msg = message_queues[s].get_nowait()
                except Queue.Empty:
                    outputs.remove(s)
                else:
                    s.send(next_msg)
            for s in exceptional:
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()
                del message_queues


class client(Thread):
    def run(self):
        TCP_IP = "127.0.0.1"
        TCP_PORT = 50000
        Buffer_size = 10054
        message = "Respect maxim coae"

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(str.encode(message))
        data = s.recv(Buffer_size)
        s.close()

        print("Primesti date:", data)


class thread_checker(Thread):
    print("Alrighty")

    def run(self):
        a_old = []
        a = []
        a = threading.enumerate()
        if a_old != a:
            print("Current threads are: \n")
            for i in threading.enumerate():
                print("\t", i)
            time.sleep(2)
            a_old = a


if __name__ == "__main__":

    server = server()
    server.start()

    client = client()
    client.start()

    threader = thread_checker()
    threader.start()











