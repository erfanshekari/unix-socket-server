from enum import Enum

class UnixSocketServerHandlerTypes(Enum):
    http = 'http'
    stream = 'stream'