import docker
from docker import DockerClient
from docker.models.containers import Container
import psycopg2 as pg
from time import sleep
from src.sql.users import generate_users_table
from src.sql.user_actions import generate_user_actions_table


class DB:
    """Class handles DB container and fills it with random data to analyze"""

    CLIENT: DockerClient
    CONTAINER: Container
    PARAMS: dict
    DATA: dict
    STATE_RUNNING: bool
    TABLES: list

    def __init__(self, db_params, data=None):
        """create instance"""
        self.PARAMS = db_params
        self.CLIENT = docker.from_env()
        self.CONTAINER = None
        self.DATA = data
        self.STATE_RUNNING = False
        self.TABLES = []

    def start(self):
        self.CONTAINER = self.CLIENT.containers.create(
            image='postgres',
            auto_remove=True,
            environment={
                'POSTGRES_PASSWORD': self.PARAMS['password'],
                'POSTGRES_DB': self.PARAMS['dbname'],
                'POSTGRES_USER': self.PARAMS['user']
            },
            name='postgres',
            ports={'5432': self.PARAMS['port']}
        )
        self.CONTAINER.start()
        self.STATE_RUNNING = True
        sleep(2)

    def stop(self):
        if self.STATE_RUNNING:
            self.CONTAINER.kill()
        self.CLIENT.close()
        self.STATE_RUNNING = False

    def query(self, query):
        with pg.connect(
            dbname=self.PARAMS['dbname'],
            host='localhost',
            port=self.PARAMS['port'],
            user=self.PARAMS['user'],
            password=self.PARAMS['password']
        ) as db_conn:
            with db_conn.cursor() as db_cursor:
                try:
                    db_cursor.execute(query)
                    result = ([col.name for col in db_cursor.description], db_cursor.fetchall())
                except Exception as ex:
                    result = str(ex)
                    print(result)
                except KeyboardInterrupt:
                    raise
            db_cursor.close()
        db_conn.close()
        return result

    def create_tables(self):
        """create all tables below"""
        self.query(generate_users_table(self.DATA))
        self.query(generate_user_actions_table(self.DATA))
        #
        tables_sql = '''SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';'''
        self.TABLES = [table_name[0] for table_name in self.query(tables_sql)[1]]


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
