from server.core.attempt2.player_client import PlayerPosition, PlayerClient


class DummyPlayer(PlayerClient):
    def __init__(self, i: int):
        self._name = f"Dummy Player Client #{i}"
        self.current_position = PlayerPosition()
        self.connection = None
        self.connection_id = i
        self.player_number = i
