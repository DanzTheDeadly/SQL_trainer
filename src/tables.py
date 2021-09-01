import random
from datetime import datetime as dt
from math import floor


def generate_users(data):
    with open('src/sql/users.sql') as sql:
        ddl = sql.read()
    dml = "INSERT INTO users (name, city, gender, regdate) " \
          "VALUES ('{name}', '{city}', '{gender}', '{regdate}');\n"
    query = ''
    for i in range(100):
        query += dml.format(
            name=random.choice(data['names']),
            city=random.choice(data['cities']),
            gender=random.choice(['M', 'F']),
            regdate=dt.fromtimestamp(
                random.randint(data['start_timestamp'], floor(dt.now().timestamp()))
            ).strftime('%Y-%m-%d %H:%M:%S')
        )
    return ddl + query


def generate_user_actions(data):
    with open('src/sql/user_actions.sql') as sql:
        ddl = sql.read()
    dml = "INSERT INTO user_actions (user_id, action, city, device, ts) " \
          "VALUES ('{user_id}', '{action}', '{city}', '{device}', '{ts}');\n"
    query = ''
    for i in range(10000):
        query += dml.format(
            user_id=random.randint(1, 200),
            action=random.choice(data['actions']),
            city=random.choice(data['cities']),
            device=random.choice(['mobile', 'pc', 'tablet']),
            ts=dt.fromtimestamp(
                random.randint(data['start_timestamp'], floor(dt.now().timestamp()))
            ).strftime('%Y-%m-%d %H:%M:%S')
        )
    return ddl + query


def generate_numbers():
    with open('src/sql/numbers.sql') as sql:
        ddl = sql.read()
    dml = "INSERT INTO numbers VALUES ({number});\n"
    query = ''
    for i in range(1, 100):
        if random.random() > 0.1:
            query += dml.format(number=i)
    return ddl + query
