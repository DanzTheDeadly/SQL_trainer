import sqlite3
from sqlite3 import Connection
from src.sql.users import generate_users_table
from src.sql.user_actions import generate_user_actions_table


class DB:
    """Class handles DB and fills it with random data to analyze"""

    CONNECTION: Connection
    DATA: dict
    STATE_RUNNING: bool
    TABLES: list

    def __init__(self, data=None):
        """create instance"""
        self.CONNECTION = None
        self.DATA = data
        self.STATE_RUNNING = False
        self.TABLES = []

    def start(self):
        self.CONNECTION = sqlite3.connect(':memory:')
        self.STATE_RUNNING = True

    def stop(self):
        self.CONNECTION.close()
        self.STATE_RUNNING = False

    def query(self, query):
        with self.CONNECTION as db_conn:
            db_cursor = db_conn.cursor()
            try:
                db_cursor.execute(query)
                result = ([col[0] for col in db_cursor.description], db_cursor.fetchall())
            except Exception as ex:
                result = str(ex)
            except KeyboardInterrupt:
                raise
            finally:
                db_cursor.close()
        return result

    def create_tables(self):
        """create all tables below"""
        with self.CONNECTION as db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.executescript(generate_users_table(self.DATA))
            db_cursor.executescript(generate_user_actions_table(self.DATA))
            #
            tables_sql = '''SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%';'''
            self.TABLES = [table_name[0] for table_name in db_cursor.execute(tables_sql)]
        db_cursor.close()
