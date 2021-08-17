import docker
from time import sleep


class DB:
    """Class handles DB container and fills it with random data to analyze"""
    def __init__(self, db_params, data=None):
        """create container"""
        self.client = docker.from_env()
        self.container = self.client.containers.create(
            image='postgres',
            auto_remove=True,
            environment={
                'POSTGRES_PASSWORD': db_params['password'],
                'POSTGRES_DB': db_params['dbname'],
                'POSTGRES_USER': db_params['user']
            },
            name='postgres',
            ports={'5432': db_params['port']}
        )
        self.data = data

    def start(self):
        self.container.start()

    def stop(self):
        self.container.kill()
        self.client.close()

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
