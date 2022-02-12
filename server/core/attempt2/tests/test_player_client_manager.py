from server.core.attempt2.player_client_manager import PlayerClientManager
from direct.distributed.PyDatagram import PyDatagram
import pytest
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from server.core.attempt2.tests.helpers import DummyPlayer


def test_datagram_minimal():
    text = "Just Some string"

    datagram = PyDatagram()
    datagram.addString(text)

    iterator = PyDatagramIterator(datagram)
    assert iterator.getString() == text


@pytest.mark.parametrize("message", ["hello world", "goodbye world"])
def test_updateChat(message):
    # Some issues with mocked methods containing assert statements
    # so we create dummy server instead
    class DummyServer:
        def __init__(self):
            pass

        def TCPPlayerSend(self, datagram, connection_id):
            iterator = PyDatagramIterator(datagram)
            assert iterator.getString() == "updateChat"
            assert iterator.getString() == message

    server = DummyServer()

    chat_datagram = PyDatagram()
    chat_datagram.addString(message)

    datagram_iter = PyDatagramIterator(chat_datagram)

    manager = PlayerClientManager()
    manager.players.append(DummyPlayer(0))
    manager.updateChat(server, datagram_iter)


updatePositionData = [
    (
        [
            {
                "x": 1,
                "y": 1,
                "z": 2,
                "h": 360,
                "p": 180,
                "r": 0,
                "is_moving": False,
                "is_grounded": True,
            },
            {
                "x": 23.5,
                "y": -12.0,
                "z": 123123,
                "h": 0.5,
                "p": 12,
                "r": 0.0002323,
                "is_moving": True,
                "is_grounded": False,
            },
        ]
    ),
    (
        [
            {
                "x": 1,
                "y": 1,
                "z": 2,
                "h": 360,
                "p": 180,
                "r": 0,
                "is_moving": False,
                "is_grounded": True,
            },
            {
                "x": 23.5,
                "y": -12.0,
                "z": 123123,
                "h": 0.5,
                "p": 12,
                "r": 0.0002323,
                "is_moving": True,
                "is_grounded": False,
            },
            {
                "x": 12312.5,
                "y": 1212.0,
                "z": 123,
                "h": 500,
                "p": 123,
                "r": 0.00022323,
                "is_moving": True,
                "is_grounded": False,
            },
            {
                "x": 23.5,
                "y": -12123.0,
                "z": 123123123,
                "h": 0.5,
                "p": 12,
                "r": 0.02323,
                "is_moving": True,
                "is_grounded": False,
            },
        ]
    ),
]


@pytest.mark.parametrize("player_data", updatePositionData)
def test_UpdatePosition(player_data):
    players = [DummyPlayer(i) for i in range(len(player_data))]

    # Some issues with mocked methods containing assert statements
    # so we create dummy server instead
    class DummyServer:
        def __init__(self):
            pass

        def TCPPlayerSend(self, datagram, connection_id):
            player = players[connection_id]

            iterator = PyDatagramIterator(datagram)
            assert iterator.getString() == "positionUpdate"
            assert iterator.getUint8() == manager.active
            for player in manager.players:
                # Player position
                assert iterator.getFloat64() == player.current_position.x
                assert iterator.getFloat64() == player.current_position.y
                assert iterator.getFloat64() == player.current_position.z

                # Player Rotation
                assert iterator.getFloat64() == player.current_position.h
                assert iterator.getFloat64() == player.current_position.p
                assert iterator.getFloat64() == player.current_position.r

    server = DummyServer()
    manager = PlayerClientManager()
    for i, player in enumerate(players):
        player.current_position.set(**player_data[i])
        manager.players.append(player)

    manager.updatePlayerPositions(server, None, force=True)
