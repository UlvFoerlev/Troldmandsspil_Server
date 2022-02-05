from server.core.helpers import getNetworkIp
from server.core.connection_manager import ConnectionManager
import socket

import logging

log = logging.getLogger(__name__)

# Used for meta data primarily
# Data that should not be lost or where individual packages is important
# such as authentication, chat, etc.
# Slower, but higher successchance, than udp. Also, tcp is ordered, udp is not
# https://realpython.com/python-sockets/#tcp-sockets
class ServerTCPCore:
    def __init__(self, port: int = 8911):
        self.server_ip = "localhost"
        self.port = port
        self.socket = None

    def open_socket(self):
        log.info(f"Opening TCP socket on {self.server_ip}:{self.port}")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.bind((self.server_ip, self.port))

        return self.socket

     def __call__(self):
        if not self.socket:
            self.open_socket()

        log.info(f"Start listening so socket on {self.server_ip}:{self.port}")
        self.socket.listen()
        conn, addr = self.socket.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
