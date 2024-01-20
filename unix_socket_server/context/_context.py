import os
from typing import Union, BinaryIO
from multiprocessing import Process
from unix_socket_server.server.server import UnixSocketServerHandlerTypes, UnixSocketServer

class UnixSocketServerContext:
    @property
    def uri(self) -> str:
        return f'unix:{self.path}'

    def __init__(
            self,
            input: Union[bytes, BinaryIO],
            path: str,
            handler: UnixSocketServerHandlerTypes = UnixSocketServerHandlerTypes.stream,
        ) -> None:
        self.path = path
        self.server = UnixSocketServer(input, handler)

    def __enter__(self):
        self.process = Process(target=self.server.listen, args=(self.path, ), daemon=True)
        self.process.start()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if hasattr(self, 'process'):
            self.process.terminate()
        try:
            os.unlink(self.path)
        except OSError:
            pass
        