import events as _events

class LocalUserActions():
    def __init__(self, world):
        self._world = world

        self._actions = {
            "id": self.setId,
            "enterTable": self.enterTable,
            "exitTable": self.exitTable,
            "joinTableError": self.joinTableError,
            "updatePlayers": self.updatePlayers,
            "openTableError": self.openTableError,
            "messageSent": self.messageSent,
            "messageCame": self.messageCame,
            "updateTablesList": self.updateTablesList,
            "updateTableState": self.updateTableState,
            "updateTableHistory": self.updateTableHistory,
            "playError": self.playError
        }

        self._events = {
            ""
        }

    async def setId(self, world, id):
        world.setId(id)

    async def execute(self, name, args):
        if name in self._actions:
            action = self._actions[ name ]
            try:
                await action(self._world, **args)
            except Exception as exc:
                print("An occured while running the action", repr(name))
        else:
            print(repr(name), ": no such action")

    async def enterTable(self, world, table):
        world.setTable(table)

    async def exitTable(self, world):
        world.setTable(None)

    async def joinTableError(self, world, message, code):
        pass

    async def updatePlayers(self, world, table, redPlayer, yellowPlayer, ghosts):
        table.tableful().update(ghosts, redPlayer, yellowPlayer)

    async def openTableError(self, world, message, code):
        pass

    async def messageSent(self, world, message):
        world.table().tableful().sendMessage(world.id(), message)

    async def messageCame(self, world, message, user):
        world.table().tableful().sendMessage(user, message)

    async def updateTablesList(self, world, tables):
        for table in tables:
            world.tables().create(table)

    async def updateTableState(self, world, state):
        world.table().setState(state)

    async def updateTableHistory(self, world, move):
        world.table().addMove(move)

    async def playError(self, world, message, code):
        pass

