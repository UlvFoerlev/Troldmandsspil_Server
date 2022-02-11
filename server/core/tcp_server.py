from server.core.helpers import getNetworkIp
from server.core.connection_manager import ConnectionManager
import socket
import selectors
import types

import logging

log = logging.getLogger(__name__)

# Used for meta data primarily
# Data that should not be lost or where individual packages is important
# such as authentication, chat, etc.
# Slower, but higher successchance, than udp. Also, tcp is ordered, udp is not
# https://realpython.com/python-sockets/#tcp-sockets
# https://realpython.com/python-sockets/#multi-connection-server
class ServerTCPCore:
    def __init__(self, port: int = 8911):
        self.server_ip = "localhost"
        self.port = port
        self.socket = None
        self.selector = selectors.DefaultSelector()

    def open_socket(self):
        log.info(f"Opening TCP socket on {self.server_ip}:{self.port}")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.bind((self.server_ip, self.port))

        self.socket.setblocking(False)

        self.selector.register(self.socket, selectors.EVENT_READ, data=None)

        return self.socket

    # Authenticate and add connection
    def authenticate(self, socket):
        # Accept everyone for now
        # Otherwise authentication code before this
        conn, addr = socket.accept()
        print("Accepted connection from", addr)
        conn.setblocking(False)

        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selector.register(conn, events, data=data)

        return True

    # Respond to authenticated connection query
    def service_connection(self, key, mask):
        socket = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:
            recv_data = socket.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb += recv_data
            else:
                # Client has closed connection, and so should we
                print("Closing connection to", data.addr)
                self.selector.unregister(socket)
                socket.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print("echoing", repr(data.outb), "to", data.addr)
                sent = socket.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]

    def __call__(self):
        if not self.socket:
            self.open_socket()

        # while True:
        while True:
            events = self.selector.select(timeout=None)
            for key, mask in events:
                print(key, mask)
                if key.data is None:
                    # If connection is self
                    if key.fileobj == self.socket:
                        print("Continued")
                        continue
                    self.authenticate(key.fileobj)

                else:
                    self.service_connection(key, mask)
            break

    def close(self):
        self.socket.close()
