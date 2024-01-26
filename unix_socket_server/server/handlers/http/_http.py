import logging
from http.server import BaseHTTPRequestHandler
from unix_socket_server.server.response import Response


class HTTPServerHandler(BaseHTTPRequestHandler):
    RESPONSE : Response

    protocol_version = 'HTTP/1.1'
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/octet-stream')
        self.send_header('Content-Length', self.RESPONSE.total_len)
        if self.RESPONSE.is_chunked:
            self.send_header('Accept-Ranges', 'bytes')
        self.end_headers()
        try:
            if self.RESPONSE.is_chunked:
                for chunk in self.RESPONSE.chunked_response:
                    self.write(chunk)
                self.write('')
            else:
                self.write(self.RESPONSE.response)
        except Exception as exc:
            logging.error(exc)

    def write(self, res) -> int:
        self.wfile.write(res)