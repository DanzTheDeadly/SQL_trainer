import random
from datetime import datetime as dt
from math import floor


def generate_user_actions_table(data):
    ddl = '''
    CREATE TABLE user_actions (
        user_id INT,
        action TEXT,
        city TEXT,
        device TEXT,
        ts TEXT
    );
    '''
    dml = 'INSERT INTO user_actions (user_id, action, city, device, ts) VALUES '
    for i in range(10000):
        random_vals = '''('{user_id}', '{action}', '{city}', '{device}', '{ts}'),'''.format(
            user_id=random.randint(1, 200),
            action=random.choice(data['actions']),
            city=random.choice(data['cities']),
            device=random.choice(['mobile', 'pc', 'tablet']),
            ts=dt.fromtimestamp(
                random.randint(data['start_timestamp'], floor(dt.now().timestamp()))
            ).strftime('%Y-%m-%d %H:%M:%S')
        )
        dml += random_vals
    dml = dml[:-1] + ';'
    return ddl + dml
