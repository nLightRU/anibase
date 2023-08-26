import os
import sqlite3
import json

# dir_path = os.path.dirname(os.path.abspath(__file__))
# data_dir = os.path.abspath(os.path.relpath('../', dir_path))\

def get_titles():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(
                            os.path.abspath(os.path.relpath('../', dir_path)),
                            'data'
                            )
    seasons_dir = os.path.join(data_dir, 'seasons_json')

    for season in os.listdir(seasons_dir):
            data = open(os.path.join(seasons_dir, season), 'r', encoding='utf-8').read()
            titles = json.loads(data)
            for title in titles:
                yield title

class Database:
    dir_path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(
                            os.path.abspath(os.path.relpath('../', dir_path)),
                            'data'
                            )

    def __init__(self, db_name):
        self.sql_path = os.path.join(Database.data_dir, 'sql')
        if not os.path.exists(os.path.join(Database.data_dir, db_name)):
            self.db_path = os.path.join(Database.data_dir, db_name)
            with sqlite3.connect(self.db_path) as con:
                script = open(os.path.join(self.sql_path, 'create_scheme.sql')).read()
                con.executescript(script)
        else:
            self.db_path = os.path.join(Database.data_dir, db_name)

    def insert_titles(self, titles):
        fields = ('mal_id', 'title', 'title_english', 'episodes',
                  'type', 'source', 'season', 'year', 'rating', 'synopsis')

        def create_insert_stmt(title):
            sql_stmt = 'INSERT INTO anime('
            values_count = 0
            for field in fields:
                if field in title.keys():
                    sql_stmt += field + ','
                    values_count += 1
            sql_stmt = sql_stmt[:-1] + ')' + 'VALUES(' + ('?, ' * (values_count -1)) + '?)'
            values = [title[field] for field in fields]

            return sql_stmt, values


        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            for title in titles:
                # we need to check if title already exists in the table
                select_stmt = 'SELECT * FROM anime WHERE mal_id = ?'
                cur.execute(select_stmt, (title['mal_id'], ))
                rows = cur.fetchall()
                if rows:
                    print(title['mal_id'], 'already exists')
                else:
                    stmt, vals = create_insert_stmt(title)
                    con.execute(stmt, vals)




if __name__ == '__main__':
    db = Database('anime_db.sqlite')
    for t in get_titles():
        db.insert_titles((t,))