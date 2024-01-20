from http.server import BaseHTTPRequestHandler

class HTTPServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/octet-stream')
        self.end_headers()
        if not type(self.RESPONSE) is bytes:
            self.wfile.write(self.RESPONSE.read())
        else:
            self.wfile.write(self.RESPONSE)