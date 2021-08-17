from http.server import BaseHTTPRequestHandler, HTTPServer
from src.db import DB


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
        self.db.start()
        self.serve_forever()

    def stop(self):
        self.db.stop()


class DBRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Response')

    def do_POST(self):
        pass
