from socketserver import BaseRequestHandler


class StreamServerHandler(BaseRequestHandler):
     def handle(self):
        if not type(self.RESPONSE) is bytes:
            self.request.sendall(self.RESPONSE.read())
        else:
            self.request.sendall(self.RESPONSE)