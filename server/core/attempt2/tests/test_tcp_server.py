from panda3d.core import (
    QueuedConnectionManager,
    QueuedConnectionListener,
    QueuedConnectionReader,
    ConnectionWriter,
)
from panda3d.core import NetDatagram, PointerToConnection, NetAddress
from direct.task.Task import Task

import logging

log = logging.getLogger(__name__)


def TCPServerCore():
    def __init__(self, port, backlog):
        self.connectionManager = QueuedConnectionManager()
        self.connectionListener = QueuedConnectionListener(self.cManager, 0)
        self.connectionReader = QueuedConnectionReader(self.cManager, 0)
        self.connectionWriter = ConnectionWriter(self.cManager, 0)

        self.port = port
        self.backlog = backlog

    def __call__(self):
        log.info(f"Starting server on {self.connectionManager.getIp()}:{self.port}")
        self.socket = self.cManager.openTCPServerRendezvous(self.port, self.backlog)
        self.connectionListener.addConnection(self.socket)

    # read incoming data
    def taskReaderPolling(self, taskdata):
        if self.connectionReader.dataAvailable():
            # Catch incoming datagram
            self.datagram = NetDatagram()

        # read datagram
        if self.connectionReader.getData(self.datagram):
            taskdata.updateData(self.datagram.getConnection(), self.datagram, self)

        return Task.cont

    # check if incoming data
    def taskListenerPolling(self, taskdata):
        # This method checks to see if there are any new clients and adds their connection
        # If theres a new connection add it to our listener
        if self.connectionListener.newConnectionAvailable():
            rendezvous = PointerToConnection()
            netAddress = NetAddress()
            newConnection = PointerToConnection()

            if self.connectionListener.getNewConnection(
                rendezvous, netAddress, newConnection
            ):
                newConnection = newConnection.p()
                # TODO: add player/connection here

                # taskdata.PlayerList.append(player())
                # taskdata.PlayerList[taskdata.active].connectionID = self.newConnection
                # taskdata.sendInitialInfo(taskdata.active, self)
                # taskdata.active += 1
                self.connectionReader.addConnection(
                    self.newConnection
                )  # Begin reading connection

        return Task.cont
