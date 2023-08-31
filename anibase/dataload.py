import os
import sqlite3
import json

from sqlalchemy.orm import Session
from sqlalchemy import update

from model import engine

db_url = '127.0.0.1:5432'
db_name = 'anibase_db'
db_user = 'anibase_app'
db_pass = 'qwerty12345'
db_uri = f'postgresql+psycopg2://{db_user}:{db_pass}@{db_url}/{db_name}'


def get_titles() -> dict:
    seasons_dir = os.path.abspath(os.path.join(os.pardir, 'data', 'seasons_json'))
    for season in os.listdir(seasons_dir):
        titles = json.loads(open(os.path.join(seasons_dir, season)).read())
        for title in titles:
            yield title


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


def insert_titles():

    from model import Anime

    def create_title_row():
        for a in get_titles():
            anime_row = Anime(mal_id=a['mal_id'], title=a['title'], title_english=a['title_english'],
                              episodes=a['episodes'], type=a['type'], source=a['source'],
                              season=a['season'], year=a['year'], rating=a['rating'], synopsis=a['synopsis'],
                              score=a['score'], members=a['members'])

            yield anime_row

    with Session(engine) as session:
        for anime_title in create_title_row():
            session.add(anime_title)
        session.commit()


def insert_genres():
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

    from model import Genre

    with Session(engine) as session:
        for genre in genres:
            genre_row = Genre(id=genre['mal_id'], name=genre['name'])
            row = session.query(Genre).filter(Genre.id == genre_row.id)
            if not row:
                session.add(genre_row)
        session.commit()


def insert_studios():
    studio_ids = set()
    studios = []
    for title in get_titles():
        for studio in title['studios']:
            if studio['mal_id'] not in studio_ids:
                studio_ids.add(studio['mal_id'])
                studios.append(studio)

    from model import Studio

    with Session(engine) as session:
        for studio in studios:
            s = Studio(id=studio['mal_id'], name=studio['name'])
            row = session.query(Studio).filter(Studio.id == s.id)
            if not row:
                session.add(s)

        session.commit()


def insert_anime_studio():

    from model import AnimeStudio
    id_row = 1
    with Session(engine) as session:
        for title in get_titles():
            for studio in title['studios']:
                session.add(AnimeStudio(id=id_row, id_anime=title['mal_id'], id_studio=studio['mal_id']))
                id_row += 1

        session.commit()


def insert_anime_genre():

    from model import AnimeGenre
    id_row = 1
    with Session(engine) as session:
        for title in get_titles():
            for genre in title['genres']:
                session.add(AnimeGenre(id=id_row, id_anime=title['mal_id'], id_genre=genre['mal_id']))
                id_row += 1

            for theme in title['themes']:
                session.add(AnimeGenre(id=id_row, id_anime=title['mal_id'], id_genre=theme['mal_id']))
                id_row += 1

        session.commit()


def update_stats():
    from model import Anime
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
    # insert_titles()
    # insert_genres()
    # insert_studios()
    # insert_anime_studio()
    # insert_anime_genre()
    # handler.update_stats()
    pass
