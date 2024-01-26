import logging, socket
from socketserver import BaseRequestHandler
from unix_socket_server.server.response import Response

class StreamServerHandler(BaseRequestHandler):
     RESPONSE : Response
     def handle(self):
        try:
            if self.RESPONSE.is_chunked:
                for chunk in self.RESPONSE.chunked_response:
                    self.request.send(chunk)
            else:
                self.request.sendall(self.RESPONSE.response)
        except Exception as exc:
            logging.error(exc)
        self.request.shutdown(socket.SHUT_WR)
        self.request.close()