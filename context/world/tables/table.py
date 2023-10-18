from .grid import *
from .move import *
from .tableful import *
import asyncio as _asyncio
import random as _random
import events as _events

class Table():
    PLAYER_YELLOW = 0
    PLAYER_RED = 1

    STATE_WAITING = 0
    STATE_PLAYING = 1
    STATE_ABANDONED = 2
    STATE_FILLED = 3

    def __init__(self, name, hidden=True):
        self._name = name
        self._grid = Grid()
        self._player = _random.choice((self.PLAYER_RED, self.PLAYER_YELLOW))
        self._hidden = hidden
        self._state = self.STATE_WAITING
        self._history = []
        self._tableful = Tableful()

        self._tableful.addEventListener("redPlayerExited", lambda userId:self.giveUp())
        self._tableful.addEventListener("yellowPlayerExited", lambda userId:self.giveUp())
        self._tableful.addEventListener("yellowPlayerCame", self._onPlayerCame)
        self._tableful.addEventListener("redPlayerCame", self._onPlayerCame)

        self._events = {
            "stateChanged": _events.EventHandler(),
            "gridChanged": _events.EventHandler(),
            "historyChanged": _events.EventHandler()
        }
    
    def tableful(self):
        return self._tableful

    def addEventListener(self, name, listener):
        self._events[ name ].connect(listener)

    def name(self):
        return self._name
    
    def _onPlayerCame(self, userId):
        if self._tableful.redPlayer() and self._tableful.yellowPlayer():
            self.start()

    def winner(self):
        lines = self._grid.lines()
        if lines:
            return lines[ 0 ].content

    def state(self):
        return self._state

    def playerTurn(self):
        return self._player

    def history(self):
        return tuple(self._history)

    def grid(self):
        return self._grid.copy()

    def start(self):
        if self._state is not self.STATE_WAITING:
            raise ValueError("table not waiting")
        self._state = self.STATE_PLAYING
        self._events[ "stateChanged" ].emit(self._state)

    def giveUp(self):
        if self._state is self.STATE_FILLED:
            raise ValueError("table already filled")

        self._state = self.STATE_ABANDONED
        self._tableful.setPlayersAsGhosts()
        self._events[ "stateChanged" ].emit(self._state)

    def setState(self, state):
        self._state = state
        self._events["stateChanged"].emit(self._state)

    def layPieceAt(self, column):
        grid = self.grid()

        self._events[ "gridChanged" ].emit(grid)

        self.addMove(PlayerMove(self._player, column))

        if grid.lines():
            self._state = self.STATE_FILLED
            self._events["stateChanged"].emit(self._state)
            return self._player

        elif not True in [ grid.pieceAt(0, i) is None for i in range(7) ]:
            self._state = self.STATE_FILLED
            self._events["stateChanged"].emit(self._state)
            return None

        if self._player is self.PLAYER_RED:
            self._player = self.PLAYER_YELLOW
        else:
            self._player = self.PLAYER_RED

        return None

    def addMove(self, move):
        grid = self.grid()
        grid.placePieceAt(move.column(), move.player())

        self._history.append(move)
        self._events[ "historyChanged" ].emit(move)


    def toJson(self):
        return {
            "name": self._name,
            "playerTurn": self._player,
            "hidden": self._hidden,
            "grid": self._grid.toJson(),
            "history": [i.toJson() for i in self._history],
            "state": self._state,
            "players": self._tableful.toJson()
        }

    def fromJson(json):
        t = Table(json[ "name" ], json[ "hidden" ])
        t._player = json[ "playerTurn" ]
        t._grid = Grid.fromJson(json[ "grid" ])
        t._history = [PlayerMove.fromJson(i) for i in json[ "history" ]]
        t._state = json[ "state" ]
        t._players = Tableful.fromJson(json[ "players" ])
        return t

