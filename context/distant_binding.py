class DistantBinding():
    def __init_(self, localActions, connection):
        self._localActions = localActions
        connection.addEventListener("open", self.onOpen)
        connection.addEventListener("message", self.onMessage)
        connection.addEventListener("error", self.onError)
        connection.addEventListener("close", self.close)

    async def onOpen(self):
        pass

    async def onMessage(self, response):
        name, args = response.name(), response.arguments()
        await self._localActions.execute(name, args)

    async def onError(self, error):
        pass

    async def onClose(self):
        pass
