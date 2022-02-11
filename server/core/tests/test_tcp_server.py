from server.core.tcp_server import ServerTCPCore
import pytest
import unittest
from server.core.tests.helpers import TCPclient


class TestTCPServer(unittest.TestCase):
    def setup(self):
        self.client = TCPclient(port=8000)

        self.server = ServerTCPCore()
        self.server()

    def close(self):
        self.client.close()
        self.server.close()

    def test_tcp_connect(self):
        self.setup()
        target_port = self.server.port
        target_address = self.server.server_ip
        self.client.connect(target_port, target_address)

        response = self.client.send("SYN")
        print(response)

        self.close()
        assert False


# def test_tcp_connection():
#     server = ServerTCPCore()

#     assert server.port == 8911

#     server()
