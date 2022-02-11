from panda3d.core import PointerToConnection
from server.core.attempt2.player_client import PlayerClient
from direct.distributed.PyDatagram import PyDatagram
from direct.showbase.ShowBaseGlobal import globalClock
from direct.distributed.PyDatagramIterator import PyDatagramIterator

# manager for player clients
class PlayerClientManager:
    def __init__(self, whitelist: list[PointerToConnection] = []):
        self.players = []
        self.timeSinceLastUpdate = 0

    def addPlayer(self, player: PlayerClient):
        # TODO: Whitelist authentication here
        self.players.append(player)

        # TODO: Return False if denied
        return True

    @property
    def active(self):
        return len(self.players)

    # Initialize the new Player
    def sendInitialInfo(self, player: PlayerClient, server):
        # NOTE: When we get spawn points and levels, the server should dictate player start position
        # TODO: Read note 🠕🠕🠕

        connection_id = player.connection_id

        # Datagram to send to client
        datagram = PyDatagram()
        datagram.addString("init")
        datagram.addUint8(player.player_number)

        # Position of all player
        for other_player in self.players:
            # Player name
            datagram.addstring(other_player.name)

            # Player position
            datagram.addFloat64(other_player.current_position.x)
            datagram.addFloat64(other_player.current_position.y)
            datagram.addFloat64(other_player.current_position.z)

            # Player Rotation
            datagram.addFloat64(other_player.current_position.h)
            datagram.addFloat64(other_player.current_position.p)
            datagram.addFloat64(other_player.current_position.r)

        server.TCPplayerSend(datagram, connection_id)

    # Keep player positions updated
    def updatePlayerPositions(self, server, data):
        # TODO: this should be  handled by UDP, not TCP
        self.elapsed = globalClock.getDt()
        self.timeSinceLastUpdate += self.elapsed
        if self.timeSinceLastUpdate > 0.1:
            # If any players is active
            if self.active > 0:
                datagram = PyDatagram()
                # datagram identifier
                datagram.addString("positionUpdate")

                # Number of active players
                datagram.addUint8(self.active)

                # Current player positions
                for player in self.players:
                    # Player position
                    datagram.addFloat64(player.current_position.x)
                    datagram.addFloat64(player.current_position.y)
                    datagram.addFloat64(player.current_position.z)

                    # Player Rotation
                    datagram.addFloat64(player.current_position.h)
                    datagram.addFloat64(player.current_position.p)
                    datagram.addFloat64(player.current_position.r)

                # Send Data
                for player in self.players:
                    server.TCPplayerSend(datagram, player.connection_id)

    # keep chat updated
    def updateChat(self, server, data):
        datagram = PyDatagram()

        # datagram identifier
        datagram.addString("updateChat")
        # Add chat text
        text = data.getString()
        self.datagram.AddString(text)

        # Send Data
        for player in self.players:
            server.TCPplayerSend(datagram, player.connection_id)

    def updatePlayers(self, server, data, identifier):
        # TODO: Should only be run if updates are received
        actions = {"positions": self.updatePlayerPositions, "chat": self.updateChat}

        return actions[identifier](server, data)

    def receivePlayerPosition(self, iterator, connection, *args):
        for player in self.players:
            if player.connection_id == connection:
                player.current_position.x = iterator.getFloat64()
                player.current_position.y = iterator.getFloat64()
                player.current_position.z = iterator.getFloat64()
                player.current_position.h = iterator.getFloat64()
                player.current_position.p = iterator.getFloat64()
                player.current_position.r = iterator.getFloat64()

    def recievePlayerChat(self, iterator, connection, server):
        self.updateChat(server, iterator)

    def receiveTCPPlayerData(self, connection, datagram, server):
        actions = {
            "chat": self.recievePlayerChat,
        }
        # TODO: verify received datagram before reading

        iterator = PyDatagramIterator(datagram)
        identifier = iterator.getString()

        return actions[identifier](iterator, connection, server)

    def receiveUDPPlayerData(self, connection, datagram, server):
        actions = {
            "positions": self.receivePlayerPosition,
        }
        # TODO: verify received datagram before reading

        iterator = PyDatagramIterator(datagram)
        identifier = iterator.getString()

        return actions[identifier](iterator, connection, server)
