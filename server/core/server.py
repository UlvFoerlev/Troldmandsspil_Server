from server.core.helpers import getNetworkIp
import socket

import logging

log = logging.getLogger(__name__)


class ServerCore:
    def __init__(self, port: int = 8910):
        self.server_ip = "localhost"
        self.port = port
        self.socket = None

    def open_socket(self):
        log.info(f"Opening socket on {self.server_ip}:{self.port}")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.socket.bind((self.server_ip, self.port))

        return self.socket

    def __call__(self):
        if not self.socket:
            self.open_socket()

        log.info(f"Start listening so socket on {self.server_ip}:{self.port}")
        with self.socket as socket:
            while True:
                bytesAddressPair = socket.recv(1024)
                if bytesAddressPair:
                    print(bytesAddressPair)

                message = bytesAddressPair[0]

                address = bytesAddressPair[1]

                clientMsg = "Message from Client:{}".format(message)
                clientIP = "Client IP Address:{}".format(address)

                print(clientMsg)
                print(clientIP)

    def exit():
        pass
