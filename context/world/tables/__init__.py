from .table import *
import random as _random
import events as _events

class TablesList():
    def __init__(self):
        self._tables = [ ]
        self._events = {
            "tableCreated": _events.EventHandler(),
            "tableDeleted": _events.EventHandler()
        }

    def addEventListener(self, name, listener):
        self._events[ name ].connect(listener)

    def getTableByName(self, name):
        for table in self._tables:
            if table.name() == name:
                return table

        return self.create(name)

    def getRandomTable(self):
        dtables = [ i for i in self._tables if not i.hidden() and i.state() is i.STATE_WAITING ]

        if not dtables:
            return self.create(False)

        return _random.choice(dtables)

    def getTables(self):
        return tuple(self._tables)
    
    def _on_table_left(self, table, ghostId):
        if table.state() is table.STATE_ABANDONED and not table.tableful().ghosts():
            self.removeTable(table)

    def create(self, jsonTable):
        table = self.getTableByName(jsonTable[ "name" ])
        if table is not None:
            self.removeTable(jsonTable[ "name" ])

        table = Table.fromJson(jsonTable)
        
        table.tableful().addEventListener("ghostExited", lambda ghostId:self._on_table_left(table, ghostId))
        
        self._tables.append(table)
        self._events[ "tableCreated" ].emit(table)
        return table

    def removeTable(self, name):
        table = self.getTableByName(name)
        if table is not None:
            self._tables.remove(table)
        self._events[ "tableDeleted" ].emit(table)

