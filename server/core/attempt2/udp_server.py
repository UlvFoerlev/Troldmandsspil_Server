from panda3d.core import (
    ConnectionManager,
    RecentConnectionReader,
    ConnectionWriter,
)
from panda3d.core import NetDatagram

import logging

log = logging.getLogger(__name__)


class UDPServerCoreMixin:
    def init_udp(self, port, backlog):
        self.UDPconnectionManager = ConnectionManager()
        self.UDPconnectionWriter = ConnectionWriter(self.UDPconnectionManager)
        self.UDPconnectionReader = RecentConnectionReader(self.UDPconnectionManager)
        self.UDPconnectionReader.setRawMode(1)

        self.port = port
        self.backlog = backlog

    def run_udp(self):
        # Run Server
        log.info(f"Starting UDP server on {self.port}")

        self.udp_socket = self.UDPconnectionManager.openUDPConnection(self.port)
        self.udp_socket.setReuseAddr(True)

    def taskUDPReaderPolling(self, task):
        if self.UDPconnectionReader.dataAvailable():
            datagram = NetDatagram()
            if self.UDPconnectionReader.getData(datagram):
                print(datagram)
                # TODO: Only accept UDP from players in player_client_manage
