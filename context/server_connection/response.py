class Response():
    def __init__(self, name, **args):
        self._name = name
        self._args = args

    def name(self):
        return self._name

    def arguments(self):
        return self._args.copy()

    def getArgument(self, name, default = None):
        if name in self._args:
            return self._args[ name ]
        else:
            return default
    