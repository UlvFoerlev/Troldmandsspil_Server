from server.core.helpers import getNetworkIp
import socket


class ServerCore:
    def __init__(self, port: int = 8910):
        self.server_ip = "localhost"
        self.port = port

    def __call__(self):
        print(f"Server started on {self.server_ip}:{self.port}")
        print("Waiting for incoming connections.")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.socket.bind((self.server_ip, self.port))

        return self.socket

    def exit():
        pass
