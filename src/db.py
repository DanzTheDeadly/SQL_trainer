import docker
import psycopg2 as pg
from time import sleep


class DB:
    """Class handles DB container and fills it with random data to analyze"""

    client: docker.DockerClient
    container: docker.models.containers.Container

    def __init__(self, db_params, data=None):
        """create container"""
        self.db_params = db_params
        self.client = docker.from_env()
        self.container = self.client.containers.create(
            image='postgres',
            auto_remove=True,
            environment={
                'POSTGRES_PASSWORD': self.db_params['password'],
                'POSTGRES_DB': self.db_params['dbname'],
                'POSTGRES_USER': self.db_params['user']
            },
            name='postgres',
            ports={'5432': self.db_params['port']}
        )
        self.data = data

    def start(self):
        self.container.start()
        sleep(2)

    def stop(self):
        self.container.kill()
        self.client.close()

    def query(self, query):
        with pg.connect(
            dbname=self.db_params['dbname'],
            host='localhost',
            port=self.db_params['port'],
            user=self.db_params['user'],
            password=self.db_params['password']
        ) as db_conn:
            with db_conn.cursor() as db_cursor:
                try:
                    db_cursor.execute(query)
                    result = db_cursor.fetchall()
                except pg.errors.SyntaxError as ex:
                    result = ex
            db_cursor.close()
        db_conn.close()
        return result

    def create_tables(self):
        """create all tables below"""
        self.create_users_table()

    def create_users_table(self):
        """create users table with random data and serial user ids"""
        pass


if __name__ == '__main__':
    # test mode
    db = DB({
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'pgpass',
        'port': '5432'
    })
    db.start()
    try:
        while True:
            sleep(1)
    except:
        db.stop()
        raise
