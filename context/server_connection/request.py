class Request():
    def __init__(self, requestName, **args):
        self._name = requestName
        self._args = args
    
    def name(self):
        return self._name
    
    def arguments(self):
        return self._args.copy()
    
    def getArgument(self, name):
        return self._args[ name ]
    
    def toJson(self):
        return {
            "name": self._name,
            "args": self._args
        }
    