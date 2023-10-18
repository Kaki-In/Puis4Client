from .tables import *

class World():
    def __init__(self):
        self._table = None
        self._tables = TablesList()

        self._id = None

    def setId(self, id):
        if self._id is not None and id is not None:
            raise ValueError("id already given")

        self._id = id

    def id(self):
        return self._id
    
    def table(self):
        return self._tables.getTableByName(self._table)
    
    def setTable(self, jsonTable):
        name = jsonTable[ "name" ]
        self._tables.create(jsonTable)
        self._table = name

    def tables(self):
        return self._tables


