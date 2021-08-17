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
    def do_GET(self, data=b''):
        self.send_response(200)
        self.end_headers()
        with open('src/index.html', 'rb') as file:
            page = file.read()
            page = page.replace(b'$DATA', data)
            self.wfile.write(page)

    def do_POST(self):
        sql = self.rfile.read(int(self.headers['Content-length'])).replace(b'SQL=', b'')
        data = str(self.server.db.query(sql)).encode()
        self.do_GET(data)
