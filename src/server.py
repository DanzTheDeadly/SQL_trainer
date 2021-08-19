from http.server import BaseHTTPRequestHandler, HTTPServer
from src.db import DB
from src.page.response import generate_http_response


class DBHttpServer(HTTPServer):
    config: dict
    db: DB
    page: str

    def __init__(self, config):
        """Eat config, start database and fill it with random data"""

        self.config = config
        self.db = DB(self.config['db_params'], self.config['data'])
        with open('src/page/index.html') as file:
            self.page = file.read()
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
            self.send_response(200)
            self.end_headers()
            self.wfile.write(self.server.page.encode())
        else:
            self.send_response(response_code)
            self.end_headers()
            self.wfile.write(html.encode())
            self.server.page = html

    def do_POST(self):
        post_request = self.rfile.read(int(self.headers['Content-length']))
        response_code, html = generate_http_response(post_request.decode('utf-8'), self.server.db)
        self.do_GET(response_code, html)
