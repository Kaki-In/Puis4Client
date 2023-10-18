import websocket as _websocket
import events as _events
import asyncio as _asyncio
import json as _json
from .request import *
from .response import *

class ServerConnection():
    def __init__(self, host, port):
        self._conn = None
        self._host = host
        self._port = port
        
        self._events = {
            "open": _events.EventHandler(),
            "message": _events.EventHandler(),
            "error": _events.EventHandler(),
            "close": _events.EventHandler()
        }
    
    def addEventListener(self, event, function):
        self._events[ event ].connect(function)
    
    def start(self):
        _asyncio.get_event_loop().create_task(self.main)
    
    def _init_connection(self):
        self._conn = _websocket.create_connection("ws://{host}:{port}/".format(host=self._host, port=self._port))
        self._events[ "open" ].emit()
    
    def _main_incoming_messages(self):
        try:
            message = self._conn.recv()
            data = _json.loads(message)
            event = Response(data[ 'name' ], **data[ "args" ])
            self._events[ "message" ].emit(event)
        except _websocket.WebSocketConnectionClosedException:
            return True
        except Exception as exc:
            self._events[ "error" ].emit(exc)
        return False
 
    def _close_connection(self):
        if self._conn is not None:
            self._conn.close()
            self._events[ "close" ].emit()
    
    async def main(self):
        self._init_connection()
        closed = False
        while not closed:
            closed = self._main_incoming_messages()
            await _asyncio.sleep(0.01)
        self._close_connection()
    
    def send(self, request):
        raw = _json.dumps(request.toJson())
        self._conn.send(raw)

    def createTable(self):
        request = Request("create")
        self.send(request)

    def openTable(self, tableName):
        request = Request("open", tableName)
        self.send(request)

    def joinTable(self, tableName=None):
        request = Request("join", tableName=tableName)
        self.send(request)

    def sendMessage(self, message):
        request = Request("sendMessage", message=message)
        self.send(request)

    def playAt(self, column):
        request = Request("playAt", column=column)
        self.send(request)

    def getTables(self):
        request = Request("getTables")
        self.send(request)

