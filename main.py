from flask import Flask, render_template, redirect, request
from src.db import DB
import yaml


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
        if db.STATE_RUNNING:
            return redirect('/')
        else:
            if request.form.get('DB_COMMAND') == 'CREATE':
                db.start()
                db.create_tables(config['data'])
                return redirect('/database')


@server.route('/database', methods=['GET', 'POST'])
def db_gui():
    # do nothing
    if request.method.upper() == 'GET':
        if db.STATE_RUNNING:
            return render_template('db_nodata.html', tables=db.TABLES)
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
                query = request.form.get('SQL')
                columns, rows = db.query(query)
                return render_template('db_data.html',
                                       tables=db.TABLES,
                                       header=columns,
                                       rows=rows,
                                       query=query)


if __name__ == '__main__':
    with open('config.yaml') as file:
        config = yaml.safe_load(file)
    server.run(debug=True, threaded=False)
