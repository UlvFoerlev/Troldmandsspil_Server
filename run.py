from server.core.udp_server import ServerUDPCore
from server.core.tcp_server import ServerTCPCore

if __name__ == "__main__":
    core = ServerTCPCore()

    core()
