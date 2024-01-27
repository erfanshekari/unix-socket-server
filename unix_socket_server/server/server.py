import os
from typing import Union, BinaryIO
from socketserver import UnixStreamServer
from ._types import UnixSocketServerHandlerTypes
from .handlers import (
    HTTPServerHandler,
    StreamServerHandler
)
from .response import Response

class UnixSocketServer:
    class UnixSocketServer(UnixStreamServer):...
        
    def __init__(
            self, 
            input: Union[bytes, BinaryIO], 
            handler: UnixSocketServerHandlerTypes = UnixSocketServerHandlerTypes.stream,
    ) -> None:
        self.input = input
        
        RESPONSE = Response(input)

        if handler == UnixSocketServerHandlerTypes.http or handler == UnixSocketServerHandlerTypes.http.value:
            self.handler = type('UnixSocketServerHTTPHandler', (HTTPServerHandler, ), dict({'RESPONSE': RESPONSE}))
        else:
            self.handler = type('UnixSocketServerStreamHandler', (StreamServerHandler, ), dict({'RESPONSE': RESPONSE}))

    def listen(self, path: str) -> None:
        self.path = path
        try:
            os.unlink(path)
        except OSError:
            if os.path.exists(path):
                raise

        self.server = self.UnixSocketServer((path), self.handler)
        self.server.serve_forever()

    def close(self) -> None:
        if hasattr(self, 'server'):
            self.server.server_close()
        
        if hasattr(self, 'path'):
            try:
                os.unlink(self.path)
            except OSError:
                pass