from panda3d.core import (
    QueuedConnectionManager,
    QueuedConnectionListener,
    QueuedConnectionReader,
    ConnectionWriter,
)
from panda3d.core import NetDatagram, PointerToConnection, NetAddress
from direct.task.Task import Task
from server.core.attempt2.player_client_manager import PlayerClientManager
from server.core.attempt2.player_client import PlayerClient


import logging

log = logging.getLogger(__name__)


class TCPServerCoreMixin:
    def init_tcp(self, port, backlog):
        self.TCPconnectionManager = QueuedConnectionManager()
        self.TCPconnectionListener = QueuedConnectionListener(
            self.TCPconnectionManager, 0
        )
        self.TCPconnectionReader = QueuedConnectionReader(self.TCPconnectionManager, 0)
        self.TCPconnectionWriter = ConnectionWriter(self.TCPconnectionManager, 0)

        self.port = port
        self.backlog = backlog

        self.client_manager = PlayerClientManager()

    def run_tcp(self):
        # Run Server
        log.info(f"Starting TCP server on {self.port}")

        self.tcp_socket = self.TCPconnectionManager.openTCPServerRendezvous(
            self.port, self.backlog
        )
        self.TCPconnectionListener.addConnection(self.tcp_socket)

    # read incoming data
    def taskTCPReaderPolling(self, task):
        if self.TCPconnectionReader.dataAvailable():
            # Catch incoming datagram
            datagram = NetDatagram()

            # read datagram
            if self.TCPconnectionReader.getData(datagram):
                self.client_manager.updateData(datagram.getConnection(), datagram, self)

        return Task.cont

    # check if incoming data
    def taskTCPListenerPolling(self, task):
        # This method checks to see if there are any new clients and adds their connection
        # If theres a new connection add it to our listener
        if self.TCPconnectionListener.newConnectionAvailable():
            rendezvous = PointerToConnection()
            netAddress = NetAddress()
            newConnection = PointerToConnection()

            if self.TCPconnectionListener.getNewConnection(
                rendezvous, netAddress, newConnection
            ):
                # Connect player
                client = PlayerClient(newConnection)

                success = self.client_manager.addPlayer(client)
                if success:
                    client.player_number = self.client_manager.active - 1
                    self.client_manager.sendInitialInfo(client, self)

                    # Begin reading connection
                    self.TCPconnectionReader.addConnection(client.connection_id)

                # TODO: Access denied message

        return Task.cont

    def TCPPlayerSend(self, datagram, connection_id):
        self.TCPconnectionWriter.send(datagram, connection_id)
