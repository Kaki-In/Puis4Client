class PlayerMove():
    def __init__(self, player, column):
        self._player = player
        self._column = column

    def player(self):
        return self._player

    def column(self):
        return self._column

    def toJson(self):
        return {
            "player": self._player,
            "column": self._column
        }

    def fromJson(json):
        return PlayerMove(json[ "player" ], json[ "column" ])
