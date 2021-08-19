from src.db import DB


def generate_http_response(post_request: str, db: DB) -> (int, str):
    html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <style>
                table, th, td {{
                    border: 1px solid gray;
                }}
                article {{
                    width: 70%;
                    margin-left:auto;
                    margin-right:auto;
                    margin-top:3%;
                }}
            </style>
            <meta charset="UTF-8">
            <title>Database GUI</title>
        </head>
        <body>
            <article>
                <p>Database GUI</p>
                {state}
                {tables}
                {form}
                {data}
            </article>
        </body>
        </html>'''

    if post_request.startswith('SQL='):
        if not db.STATE_RUNNING:
            return 400, ''
        else:
            query_result = db.query(post_request.replace('SQL=', ''))
            if type(query_result) == str:
                data = '<p>ERROR: {}</p>'.format(str(query_result))
            else:
                column_names = query_result[0]
                rows = query_result[1]
                table_header = '<tr>{header}</tr>'.format(header=''.join(['<th>{}</th>'.format(colname) for colname in column_names]))
                table_rows = ''
                for row in rows:
                    table_rows += '<tr>{row}</tr>\n'.format(row=''.join(['<td>{}</td>'.format(cell) for cell in row]))
                data = '''
                    <table>
                        {header}
                        {rows}
                    </table>
                '''.format(header=table_header, rows=table_rows)
            state = '<p>Database UP</p>'
            tables = '<p>Database tables: {}</p>'.format(', '.join(db.TABLES))
            form = '''
                </form>
                    <form method="post">
                    <input type="submit" name="DB_SIGNAL" value="Stop Database"></input>
                </form>
                <br></br>
                <form method="post" enctype="text/plain">
                    <input type="text" name="SQL">
                    <button type="submit">Submit query</button>
                </form>
            '''
            return 200, html.format(state=state, tables=tables, form=form, data=data)

    elif post_request.startswith('DB_SIGNAL='):
        if not db.STATE_RUNNING:
            db.start()
            db.create_tables()
            state = '<p>Database UP</p>'
            tables = '<p>Database tables: {}</p>'.format(', '.join(db.TABLES))
            form = '''
                </form>
                    <form method="post">
                    <input type="submit" name="DB_SIGNAL" value="Stop Database"></input>
                </form>
                <br></br>
                <form method="post" enctype="text/plain">
                    <input type="text" name="SQL">
                    <button type="submit">Submit query</button>
                
            '''
            data = ''
            return 200, html.format(state=state, tables=tables, form=form, data=data)
        else:
            db.stop()
            state = '<p>Database DOWN</p>'
            tables = ''
            form = '''
                <form method="post">
                    <input type="submit" name="DB_SIGNAL" value="Start Database"></input>
                </form>
            '''
            data = ''
            return 200, html.format(state=state, tables=tables, form=form, data=data)
    else:
        return 400, ''
