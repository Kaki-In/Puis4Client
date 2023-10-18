import events as _events
import random as _random

class Tableful():
    def __init__(self):
        self._ghosts = []
        self._redPlayer = None
        self._yellowPlayer = None
        
        self._events = {
            "message": _events.EventHandler(),
            "ghostCame": _events.EventHandler(),
            "ghostExited": _events.EventHandler(),
            "redPlayerCame": _events.EventHandler(),
            "redPlayerExited": _events.EventHandler(),
            "yellowPlayerCame": _events.EventHandler(),
            "yellowPlayerExited": _events.EventHandler()
        }
    
    def addEventListener(self, event, function):
        self._events[ event ].connect(function)
    
    def sendMessage(self, message, userId):
        self._events[ "message" ].emit(message, userId)
    
    def ghosts(self):
        return tuple(self._ghosts)
    
    def redPlayer(self):
        return self._redPlayer
    
    def yellowPlayers(self):
        return self._yellowPlayer
    
    def addGhost(self, userId):
        self._ghosts.append(userId)
        self._events[ "ghostCame" ].emit(userId)
    
    def removeGhost(self, userId):
        self._ghosts.remove(userId)
        self._events[ "ghostExit" ].emit(userId)

    def setRedPlayer(self, userId):
        self._redPlayer = userId
        if userId is None:
            self._events["redPlayerExited"].emit()
        else:
            self._events["redPlayerCame"].emit(userId)

    def setYellowPlayer(self, userId):
        self._yellowPlayer = userId
        if userId is None:
            self._events[ "yellowPlayerExited" ].emit()
        else:
            self._events[ "yellowPlayerCame" ].emit(userId)

    def removeRedPlayer(self):
        self._redPlayer = None
        self._events[ "redPlayerExited" ].emit()
    
    def removeYellowPlayer(self):
        self._yellowPlayer = None
        self._events[ "yellowPlayerExited" ].emit()
    
    def setPlayersAsGhosts(self):
        r, y = self._redPlayer, self._yellowPlayer
        self.addGhost(r)
        self.removeRedPlayer()
        self.addGhost(y)
        self.removeYellowPlayer()
    
    def toJson(self):
        return {
            "ghosts": self._ghosts,
            "redPlayer": self._redPlayer,
            "yellowPlayer": self._yellowPlayer
        }

    def update(self, ghosts, redPlayer, yellowPlayer):
        for ghost in ghosts:
            if not ghost in self._ghosts:
                self.removeGhost(ghost)

        for ghost in self._ghosts:
            if not ghost in ghosts:
                self.addGhost(ghost)

        if redPlayer is not self.redPlayer():
            self.setRedPlayer(redPlayer)

        if yellowPlayer is not self.yellowPlayers():
            self.setYellowPlayer(yellowPlayer)

    def fromJson(json):
        t = Tableful()
        t._ghosts = json[ "ghosts" ]
        t._redPlayer = json[ "redPlayer" ]
        t._yellowPlayer = json[ "yellowPlayer" ]
