import os
from typing import Union, BinaryIO
from socketserver import UnixStreamServer
from ._types import UnixSocketServerHandlerTypes
from .handlers import (
    HTTPServerHandler,
    StreamServerHandler
)
from ._exceptions import (
    UnableToHandleInput,
    InputIsNotReadable
)

class UnixSocketServer:
    class UnixSocketServer(UnixStreamServer):
        def get_request(self):
            request, _ = super().get_request()
            return (request, ["local", 0])
        
    def __init__(
            self, 
            input: Union[bytes, BinaryIO], 
            handler: UnixSocketServerHandlerTypes = UnixSocketServerHandlerTypes.stream,
    ) -> None:
        self.input = input
        if not type(self.input) is bytes:
            if not hasattr(self.input, 'read') or not hasattr(self.input, 'readable'):
                raise UnableToHandleInput()
            if not self.input.readable():
                raise InputIsNotReadable()


        if handler == UnixSocketServerHandlerTypes.http:
            self.handler = type('UnixSocketServerHTTPHandler', (HTTPServerHandler, ), dict({'RESPONSE': self.input}))
        else:
            self.handler = type('UnixSocketServerStreamHandler', (StreamServerHandler, ), dict({'RESPONSE': self.input}))

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