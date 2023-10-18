from .lines import *
from copy import deepcopy as _deepcopy

class Grid():
    def __init__(self):
        self._grid = [ [None for _ in range(6)] for _ in range(7) ]

    def isCompleted(self):
        return self.lines or not None in [ self.pieceAt(0, i) for i in range(7) ]

    def placePieceAt(self, column_number, player):
        column = self._grid[ column_number ]
        if column[ 0 ]:
            raise ValueError("column already filled")

        for i in range(5):
            if column[ i + 1 ] is not None:
                break
            i += 1

        column[ i ] = player

    def pieceAt(self, line, column):
        return self._grid[ column ][ line ]

    def lines(self):
        directions = [(1, 0), (1, 1), (1, -1), (0, 1)]
        lines = []
        for direction in directions:
            for xstart in range(7):
                if not (0 <= xstart + direction[ 0 ] * 3 < 7):
                    continue
                for ystart in range(6):
                    if not (0 <= ystart + direction[ 1 ] * 3 < 6):
                        continue

                    piece = self.pieceAt(ystart, xstart)
                    if piece is None: continue
                    line = True
                    for piece_index in range(1, 4):
                        if self.pieceAt(ystart + direction[ 1 ] * piece_index, xstart + direction[ 0 ] * piece_index) is not piece:
                            line = False
                            break
                    if line:
                        lines.append(Line(xstart, ystart, *direction, piece))
        return lines

    def copy(self):
        grid = Grid()
        grid._grid = _deepcopy(self._grid)
        return grid

    def __str__(self):
        a = ""
        for line in range(6):
            for column in range(7):
                a += "│"
                piece = self._grid[ column ][ line ]
                if piece is None:
                    a += " "
                elif piece:
                    a += "╳"
                else:
                    a += "◯"
            a += "│\n"
        a += "└─" + ("┴─") * 6 + "┘"
        return a

    def toJson(self):
        return self._grid

