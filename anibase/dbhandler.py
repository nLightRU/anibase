import os
import sqlite3
import json

import sqlalchemy.exc
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def get_organisations(organisation: str) -> list[dict]:
    """

    :param organisation:
    :return:
    """
    assert (organisation in ('studios', 'licensors', 'producers'))

    seasons_dir = os.path.abspath(os.path.join(os.pardir, 'data', 'seasons_json'))
    titles = []
    for season in os.listdir(seasons_dir):
        titles.extend(json.loads(open(os.path.join(seasons_dir, season)).read()))

    orgs_id = set()
    orgs = []
    for title in titles:
        for o in title[organisation]:
            if o['mal_id'] not in orgs_id:
                orgs_id.add(o['mal_id'])
                orgs.append(o)

    return orgs


def get_anime_organisations(mal_id, year, season, organisation) -> list[dict]:
    """

    :param mal_id:
    :param year:
    :param season:
    :param organisation:
    :return: list of dicts with data about studios / producers or empty list
    """
    seasons_dir = os.path.abspath(os.path.join(os.pardir, 'data', 'seasons_json'))
    for file in os.listdir(seasons_dir):
        y, s = file[:-5].split('_')
        if year == int(y) and season == s:
            titles = json.loads(open(os.path.join(seasons_dir, file)).read())
            break
    else:
        return []

    for title in titles:
        if title['mal_id'] == mal_id and organisation in title.keys():
            return title[organisation]
        else:
            return []


class DBHandler:
    dir_path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(
        os.path.abspath(os.path.relpath('../', dir_path)),
        'data'
    )

    seasons_dir = os.path.abspath(os.path.join(os.pardir, 'data', 'seasons_json'))

    def __init__(self, db_name):
        self.sql_path = os.path.join(DBHandler.data_dir, 'sql')
        if not os.path.exists(os.path.join(DBHandler.data_dir, db_name)):
            self.db_path = os.path.join(DBHandler.data_dir, db_name)
            with sqlite3.connect(self.db_path) as con:
                script = open(os.path.join(self.sql_path, 'create_scheme.sql')).read()
                con.executescript(script)
        else:
            self.db_path = os.path.join(DBHandler.data_dir, db_name)

    @staticmethod
    def _get_titles() -> dict:
        for season in os.listdir(DBHandler.seasons_dir):
            titles = json.loads(open(os.path.join(DBHandler.seasons_dir, season)).read())
            for title in titles:
                yield title

    def insert_genres(self):
        genres_ids = set()
        genres = []
        for title in DBHandler._get_titles():
            for genre in title['genres']:
                if genre['mal_id'] not in genres_ids:
                    genres_ids.add(genre['mal_id'])
                    genres.append(genre)

            for theme in title['themes']:
                if theme['mal_id'] not in genres_ids:
                    genres_ids.add(theme['mal_id'])
                    genres.append(theme)

        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            for genre in genres:
                select_stmt = 'SELECT id FROM genre WHERE id=?'
                row = cur.execute(select_stmt, (genre['mal_id'],)).fetchone()

                if not row:
                    cur.execute('INSERT INTO genre(id, name) VALUES(?, ?)',
                                (genre['mal_id'], genre['name'])
                                )

    def insert_studios(self):
        studio_ids = set()
        studios = []
        for title in DBHandler._get_titles():
            for studio in title['studios']:
                if studio['mal_id'] not in studio_ids:
                    studio_ids.add(studio['mal_id'])
                    studios.append(studio)

        from model import db
        from model import Studio

        engine = create_engine('sqlite:///'+self.db_path)

        try:
            db.metadata.tables['studio'].create(bind=engine)
        except sqlalchemy.exc.OperationalError:
            print('Table already exists')

        with Session(engine) as session:
            for studio in studios:
                s = Studio(id=studio['mal_id'], name=studio['name'])
                row = session.query(Studio).filter(Studio.id == s.id)
                if not row:
                    session.add(s)

            session.commit()

    def insert_titles(self, titles):
        fields = ('mal_id', 'title', 'title_english', 'episodes',
                  'type', 'source', 'season', 'year', 'rating', 'synopsis')

        def create_insert_stmt(anime_title):
            sql_stmt = 'INSERT INTO anime('
            values_count = 0
            for field in fields:
                if field in anime_title.keys():
                    sql_stmt += field + ','
                    values_count += 1
            sql_stmt = sql_stmt[:-1] + ')' + 'VALUES(' + ('?, ' * (values_count - 1)) + '?)'
            values = [anime_title[field] for field in fields]

            return sql_stmt, values

        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            for title in titles:
                # we need to check if title already exists in the table
                select_stmt = 'SELECT * FROM anime WHERE mal_id = ?'
                cur.execute(select_stmt, (title['mal_id'],))
                rows = cur.fetchall()
                if rows:
                    print(title['mal_id'], 'already exists')
                else:
                    stmt, vals = create_insert_stmt(title)
                    con.execute(stmt, vals)


if __name__ == '__main__':
    # print(*get_organisations('studios'), sep='\n')
    handler = DBHandler('anime_db.sqlite')
    # handler.insert_genres()
    handler.insert_studios()
