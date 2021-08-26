from src.db import DB


def generate_get_response(db: DB) -> (int, str):
    with open('src/html/style.css') as file:
        style = file.read()

    if db.STATE_RUNNING:
        with open('src/html/data.html') as file:
            html = file.read()
        # send empty table
        tables = ', '.join(db.TABLES)
        header = '<tr><th>Data</th></tr>'
        return 200, html.format(
            style=style,
            tables=tables,
            header=header,
            rows='',
            query=''
        )
    else:
        # send start html
        with open('src/html/index.html') as file:
            html = file.read()
        return 200, html.format(style=style)


def generate_post_response(post_request: str, db: DB) -> (int, str):
    with open('src/html/style.css') as file:
        style = file.read()

    if post_request.startswith('SQL='):
        query = post_request.replace('SQL=', '').strip()
        with open('src/html/data.html') as file:
            html = file.read()
        # send sql
        if not db.STATE_RUNNING:
            # bad request when sending sql to offline DB
            return 400, ''
        else:
            # process request and send data
            query_result = db.query(query)
            if type(query_result) == str:
                # error in query
                header = '<tr><th>ERROR</th></tr>\n'
                rows = '<tr><td>{error}</td></tr>'.format(error=str(query_result))
            else:
                # return data
                table_columns = query_result[0]
                table_rows = query_result[1]
                header = '<tr>' + ''.join(['<th>{}</th>'.format(col_name) for col_name in table_columns]) + '</tr>\n'
                rows = ''
                for row in table_rows:
                    rows += '<tr>' + ''.join(['<td>{}</td>'.format(cell) for cell in row]) + '</tr>\n'
            tables = ', '.join(db.TABLES)
            return 200, html.format(
                style=style,
                tables=tables,
                header=header,
                rows=rows,
                query=query
            )

    elif post_request.startswith('DB_SIGNAL='):
        # turn db on/off
        if not db.STATE_RUNNING:
            # turn on
            with open('src/html/data.html') as file:
                html = file.read()
            db.start()
            db.create_tables()
            tables = ', '.join(db.TABLES)
            header = '<tr><th>Data</th></tr>'
            return 200, html.format(
                style=style,
                tables=tables,
                header=header,
                rows='',
                query=''
            )
        else:
            # turn off
            with open('src/html/index.html') as file:
                html = file.read()
            db.stop()
            return 200, html.format(style=style)
    else:
        return 400, ''
