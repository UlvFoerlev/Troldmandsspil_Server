from server.core.helpers import getNetworkIp
import socket


class ServerCore:
    def __init__(self, port: int = 18818):
        self.server_ip = getNetworkIp()
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.bind((self.server_ip, self.port))
        except socket.error as e:
            str(e)

        self.socket.listen(2)
        print("Waiting for a connection, Server Started")

    def exit():
        pass
