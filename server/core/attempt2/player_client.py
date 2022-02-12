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

    def set(
        self,
        x=None,
        y=None,
        z=None,
        h=None,
        p=None,
        r=None,
        is_moving=None,
        is_grounded=None,
    ):
        self.x = x if x is not None else self.x
        self.y = y if y is not None else self.y
        self.z = z if z is not None else self.z
        self.h = h if h is not None else self.h
        self.p = p if p is not None else self.p
        self.r = r if r is not None else self.r
        self.is_moving = is_moving if is_moving is not None else self.is_moving
        self.is_grounded = is_grounded if is_grounded is not None else self.is_grounded

        for attr in (x, y, z, h, p, r, is_moving, is_grounded):
            if attr is not None:
                return True

        return False

    def __str__(self):
        return f"""PlayerPosition[
    Position[{self.x}, {self.y}, {self.z}],
    Rotation[{self.h}, {self.p}, {self.r}],
    Variables[
        is_moving[{self.is_moving}],
        is_grounded[{self.is_grounded}]]
]"""


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
