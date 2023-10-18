from .world import *
from .local_actions import *
from .server_connection import *
from .distant_binding import *

class Context():
    def __init__(self):
        self._world = World()
        self._localActions = LocalUserActions(world)
        self._serverConnection = None
        self._bind = None

    def world(self):
        return self._world

    def localActions(self):
        return self._localActions

    def serverConnection(self):
        return self._serverConnection

    def distantBinding(self):
        return self._bind

    def loadConnection(self, world):
        self._serverConnection = ServerConnection("chat.flopcreation.fr", 11330)
        self._bind = DistantBinding(self._localActions, self._serverConnection)

        self._serverConnection.addEventListener("close", self.loadConnection)



