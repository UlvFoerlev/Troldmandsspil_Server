# from re import S
# import socket
# target_host = "0.0.0.0"
# target_port = 27700
# # create a socket connection
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # let the client connect
# client.connect((target_host, target_port))
# # send some data
# client.send("SYN")
# # get some data
# response = client.recv(4096)
# print response
import socket


class TCPclient:
    def __init__(self, port=8000):
        self.port = port

    def connect(self, target_port, target_address):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connection = self.socket.connect((target_address, target_port))

    def send(self, data):
        self.socket.send(data)

        # Await response
        response = self.socket.recv(4096)
        return response

    def close(self):
        self.socket.close()
