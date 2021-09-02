import random
from datetime import datetime as dt
from math import floor


def generate_users(data):
    with open('src/sql/users.sql') as sql:
        ddl = sql.read()
    dml = "INSERT INTO users (name, city, gender, regdate) " \
          "VALUES ('{name}', '{city}', '{gender}', '{regdate}');\n"
    query = ''
    for i in range(data['users_count']):
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
            user_id=random.randint(1, data['users_count']+1),
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


def generate_friends(data):
    with open('src/sql/friends_duplicates.sql') as sql_dups:
        ddl_dups = sql_dups.read()
    with open('src/sql/friends.sql') as sql:
        ddl = sql.read()
    dml = "INSERT INTO friends_duplicates VALUES ({user_id}, {friend_id});\n"
    dml_no_dups = '''
        INSERT INTO friends
        SELECT
          user_id
        , friend_id
        FROM friends_duplicates t1
        EXCEPT
        SELECT
          friend_id
        , user_id
        FROM friends_duplicates;\n
    '''
    drop_dups_table = 'DROP TABLE friends_duplicates;\n'
    query = ''
    for i in range(1, data['users_count']+1):
        # some users will not have friends
        if random.random() < 0.2:
            continue
        for j in range(random.randint(1, 5)):
            query += dml.format(user_id=i, friend_id=random.randint(1, data['users_count']))
    return ddl_dups + ddl + query + dml_no_dups + drop_dups_table
