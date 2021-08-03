from http.server import BaseHTTPRequestHandler, HTTPServer


class DBRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Response')

    def do_POST(self):
        pass


class DBHttpServer(HTTPServer):
    def __init__(self):
        super().__init__(('localhost', 8080), DBRequestHandler)

    def run(self):
        self.serve_forever()