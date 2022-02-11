from panda3d.core import PointerToConnection
from typing import Optional


class PlayerPosition:
    def __init__(self):
        # Position
        self.x = None
        self.y = None
        self.z = None

        # Rotation
        self.h = None
        self.p = None
        self.r = None

        self.is_moving = False
        self.is_grounded = False  # Jumping or Falling


# Container class for player connections
class PlayerClient:
    def __init__(self, connection: PointerToConnection, name: Optional[str] = None):
        self._name = name
        self.current_position = PlayerPosition()
        self.connection = connection
        self.connection_id = connection.p()
        self.player_number = None

    @property
    def name(self):
        if self._name:
            return self.name
        else:
            return "Unnamed Player"

    @name.setter
    def name(self, new_name: str):
        self._name = new_name
