from server.core.attempt2.tcp_server import TCPServerCoreMixin
from server.core.attempt2.udp_server import UDPServerCoreMixin


class ServerCore(TCPServerCoreMixin, UDPServerCoreMixin):
    def __init__(self, port, backlog):
        self.init_tcp(port, backlog)
        self.init_udp(port, backlog)

    def __call__(self):
        self.run_tcp()
        self.run_udp()
