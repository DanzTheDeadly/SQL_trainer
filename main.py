from flask import Flask, render_template, redirect, request, abort
from src.db import DB
import yaml
import os


server = Flask('SQL Trainer')
db = DB()


@server.route('/', methods=['GET', 'POST'])
def index():
    # do nothing
    if request.method.upper() == 'GET':
        if db.STATE_RUNNING:
            return redirect('/database')
        else:
            return render_template('index.html')
    # create db
    elif request.method.upper() == 'POST':
        if not db.STATE_RUNNING:
            if request.form.get('DB_COMMAND') == 'CREATE':
                db.start()
                db.create_tables(config['data'])
                return redirect('/database')
            else:
                return abort(400)
        else:
            return abort(400)


@server.route('/database', methods=['GET', 'POST'])
def db_gui():
    # do nothing
    if request.method.upper() == 'GET':
        if db.STATE_RUNNING:
            return render_template('base_data.html',
                                   tables=db.TABLES,
                                   query_lines_num=15)
        else:
            return redirect('/')
    # process commands
    elif request.method.upper() == 'POST':
        if db.STATE_RUNNING:
            # shutdown db
            if request.form.get('DB_COMMAND') == 'DELETE':
                db.stop()
                return redirect('/')
            # return table with data
            else:
                query = request.form.get('SQL').strip()
                query_lines_num = 15 if query.count('\n') < 14 else query.count('\n')+1
                columns, rows = db.query(query)
                return render_template('result_data.html',
                                       tables=db.TABLES,
                                       header=columns,
                                       rows=rows,
                                       query_lines_num=query_lines_num,
                                       query=query)
        else:
            return abort(400)


@server.route('/example<int:num>')
def example(num):
    total_examples = 3
    with open(os.path.join(os.path.dirname(__file__), 'examples', 'example{}.sql'.format(num))) as query_file:
        query = query_file.read()
    with open(os.path.join(os.path.dirname(__file__), 'examples', 'example{}.txt'.format(num))) as descr_file:
        descr = descr_file.read()
    query_lines_num = 15 if query.count('\n') < 14 else query.count('\n')+1
    return render_template('example.html',
                            num=num,
                            total_examples=total_examples,
                            query_lines_num=query_lines_num,
                            query=query,
                            descr=descr)


if __name__ == '__main__':
    with open('config.yaml') as file:
        config = yaml.safe_load(file)
    server.run(debug=True, threaded=False)
