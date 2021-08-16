import docker
from datetime import datetime as dt, timedelta as td
import random
import psycopg2 as pg


class DB:
    """Class handles DB container and fills it with random data to analyze"""
    def __init__(self):
        """create container"""
        self.client = docker.from_env()
        self.container = self.client.containers.run(
            'postgres',
            auto_remove=True,
            detach=True,
            environment={'POSTGRES_PASSWORD': 'pgpass'},
            name='postgres'
        )

    def create_tables(self):
        """create all tables below"""
        pass

    def create_users_table(self):
        """create users table with random data and serial user ids"""
        with open('sql/users.sql') as f:
            sql = f.read()
        pass