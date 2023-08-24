import os
import csv
import sqlite3
import json

# dir_path = os.path.dirname(os.path.abspath(__file__))
# data_dir = os.path.abspath(os.path.relpath('../', dir_path))\

def read_titles():
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
            self.db_path = os.path.join(Database.data_dir, 'anime_db.dat')
            con = sqlite3.connect(self.db_path)
            con.close()


if __name__ == '__main__':
    for title in read_titles():
        print(title['mal_id'])
