import pysqlite3 as sqlite3
from sqlite3 import Connection
from src.tables import \
    generate_users, \
    generate_user_actions, \
    generate_numbers, \
    generate_friends


class DB:
    """Class handles DB and fills it with random data to analyze"""

    CONNECTION: Connection
    STATE_RUNNING: bool
    TABLES: list

    def __init__(self):
        """create instance"""
        self.STATE_RUNNING = False
        self.TABLES = []

    def start(self):
        self.CONNECTION = sqlite3.connect(':memory:')
        self.STATE_RUNNING = True

    def stop(self):
        self.CONNECTION.close()
        self.STATE_RUNNING = False

    def query(self, query):
        if not query:
            result = (['ERROR'], [('Empty query',)])
        else:
            with self.CONNECTION as db_conn:
                db_cursor = db_conn.cursor()
                try:
                    db_cursor.execute(query)
                    result = ([col[0] for col in db_cursor.description], db_cursor.fetchall())
                except sqlite3.Error as ex:
                    result = (['ERROR'], [(str(ex),)])
                except KeyboardInterrupt:
                    raise
                finally:
                    db_cursor.close()
        return result

    def create_tables(self, data):
        """create all tables below"""
        with self.CONNECTION as db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.executescript(generate_users(data))
            db_cursor.executescript(generate_user_actions(data))
            db_cursor.executescript(generate_numbers())
            db_cursor.executescript(generate_friends(data))
            #
            tables_sql = '''SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%';'''
            self.TABLES = [table_name[0] for table_name in db_cursor.execute(tables_sql)]
        db_cursor.close()
