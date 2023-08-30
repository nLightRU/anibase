import os
import sqlite3
import json

import sqlalchemy.exc
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import update


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


def get_titles() -> dict:
    seasons_dir = os.path.abspath(os.path.join(os.pardir, 'data', 'seasons_json'))
    for season in os.listdir(seasons_dir):
        titles = json.loads(open(os.path.join(DBHandler.seasons_dir, season)).read())
        for title in titles:
            yield title

def insert_titles(self):

    from model import Anime

    def create_title_row():
        for a in get_titles():
            anime_title = Anime(mal_id=a['mal_id'], title=a['title'], title_english=a['title_english'],
                            episodes=a['episodes'], type=a['type'], source=a['source'],
                            season=a['season'], year=a['year'], rating=a['rating'], synopsis=a['synopsis'],
                            score=a['score'], members=a['members'])

            yield anime_title

    engine = create_engine(DBHandler.db_uri)
    with Session(engine) as session:
        for a in create_title_row():
            session.add(a)
        session.commit()


class DBHandler:
    dir_path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(
        os.path.abspath(os.path.relpath('../', dir_path)),
        'data'
    )

    seasons_dir = os.path.abspath(os.path.join(os.pardir, 'data', 'seasons_json'))

    db_url = '127.0.0.1:5432'
    db_name = 'anibase_db'
    db_user = 'anibase_app'
    db_pass = 'qwerty12345'
    db_uri = f'postgresql+psycopg2://{db_user}:{db_pass}@{db_url}/{db_name}'

    def __init__(self, db_name):
        self.sql_path = os.path.join(DBHandler.data_dir, 'sql')
        if not os.path.exists(os.path.join(DBHandler.data_dir, db_name)):
            self.db_path = os.path.join(DBHandler.data_dir, db_name)
            with sqlite3.connect(self.db_path) as con:
                script = open(os.path.join(self.sql_path, 'create_scheme.sql')).read()
                con.executescript(script)
        else:
            self.db_path = os.path.join(DBHandler.data_dir, db_name)

    def insert_genres(self):
        genres_ids = set()
        genres = []
        for title in get_titles():
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
        for title in get_titles():
            for studio in title['studios']:
                if studio['mal_id'] not in studio_ids:
                    studio_ids.add(studio['mal_id'])
                    studios.append(studio)

        from model import db
        from model import Studio

        # TO DO: fix path again (if we start not from anibase
        # it's not opened
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

    def insert_anime_genre(self):

        from model import AnimeGenre
        id_row = 1
        engine = create_engine('sqlite:///' + self.db_path)
        with Session(engine) as session:
            for title in get_titles():
                for genre in title['genres']:
                    session.add(AnimeGenre(id=id_row, id_anime=title['mal_id'], id_genre=genre['mal_id']))
                    id_row += 1

                for theme in title['themes']:
                    session.add(AnimeGenre(id=id_row, id_anime=title['mal_id'], id_genre=theme['mal_id']))
                    id_row += 1

            session.commit()

    def insert_anime_studio(self):

        from model import AnimeStudio
        id_row = 1
        engine = create_engine('sqlite:///' + self.db_path)
        with Session(engine) as session:
            for title in get_titles():
                for studio in title['studios']:
                    session.add(AnimeStudio(id=id_row, id_anime=title['mal_id'], id_studio=studio['mal_id']))
                    id_row += 1

            session.commit()

    def update_stats(self):
        from model import Anime
        engine = create_engine('sqlite:///' + self.db_path)
        with Session(engine) as session:
            for anime in get_titles():
                score_val = anime['score']
                members_val = anime['members']
                if score_val:
                    session.execute(update(Anime).where(Anime.mal_id == anime['mal_id']).values(score=score_val))
                if members_val:
                    session.execute(update(Anime).where(Anime.mal_id == anime['mal_id']).values(members=members_val))
            session.commit()


if __name__ == '__main__':
    # print(*get_organisations('studios'), sep='\n')
    handler = DBHandler('anime_db.sqlite')
    insert_titles()
    # handler.insert_genres()
    # handler.insert_studios()
    # handler.insert_anime_genres()
    # handler.insert_anime_studio()
    # handler.update_stats()
