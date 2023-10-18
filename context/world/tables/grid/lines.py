class Line():
    def __init__(self, x, y, dx, dy, content):
        self._coords = (x, y)
        self._direction = (dx, dy)
        self._content = content

    def content(self):
        return self._content

    def x(self):
        return self._coords[ 0 ]

    def y(self):
        return self._coords[ 1 ]

    def directionX(self):
        return self._direction[ 0 ]

    def directionY(self):
        return self._direction[ 1 ]

    def __repr__(self):
        a = "<Line"
        a += " from=" + repr(self._coords)
        a += " to=" + repr(self._direction)
        a += " content=" + repr(self._content)
        return a + ">"
