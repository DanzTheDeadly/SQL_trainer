from http.server import BaseHTTPRequestHandler, HTTPServer
from src.db import DB
from src.html.response import generate_get_response, generate_post_response


class DBHttpServer(HTTPServer):
    config: dict
    db: DB

    def __init__(self, config):
        """Eat config, start database and fill it with random data"""

        self.config = config
        self.db = DB(self.config['db_params'], self.config['data'])
        super().__init__(
            (self.config['server_params']['host'], self.config['server_params']['port']),
            DBRequestHandler
        )

    def run(self):
        print('HTTP server ready')
        self.serve_forever()

    def stop(self):
        self.db.stop()


class DBRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self, response_code=None, html=None):
        if not response_code and not html:
            response_code, html = generate_get_response(self.server.db)
            self.send_response(response_code)
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            self.send_response(response_code)
            self.end_headers()
            self.wfile.write(html.encode())

    def do_POST(self):
        post_request = self.rfile.read(int(self.headers['Content-length']))
        response_code, html = generate_post_response(post_request.decode('utf-8'), self.server.db)
        self.do_GET(response_code, html)
