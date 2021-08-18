import random
from datetime import datetime as dt
from math import floor


def generate_users_table(data):
    ddl = '''
    CREATE TABLE users (
        user_id SERIAL,
        name TEXT,
        city TEXT,
        gender TEXT,
        regdate TEXT
    );
    '''
    dml = 'INSERT INTO users (name, city, gender, regdate) VALUES '
    for i in range(1000):
        random_vals = '''('{name}', '{city}', '{gender}', '{regdate}'),'''.format(
            name=random.choice(data['names']),
            city=random.choice(data['cities']),
            gender=random.choice(['M', 'F']),
            regdate=dt.fromtimestamp(random.randint(1609448400, floor(dt.now().timestamp()))).strftime('%Y-%m-%d %H:%M:%S')
        )
        dml += random_vals
    dml = dml[:-1] + ';'
    return ddl + dml
