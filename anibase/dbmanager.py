from typing import Iterable, Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class DBManager:
    def __init__(self, database, user, password):
        try:
            self.engine = create_engine(f'postgresql+psycopg2://{user}:{password}@localhost/{database}')
        except SQLAlchemyError as error:
            print(f'DBManager init caused an error {error}')

    def create_anime_table(self):
        from .model import Base, Anime

        Base.metadata.create_all(self.engine, tables=[Anime.__table__])

    def create_genre_table(self):
        from .model import Base, Genre

        Base.metadata.create_all(self.engine, tables=[Genre.__table__])

    def create_anime_genre_table(self):
        from .model import Base, AnimeGenre

        Base.metadata.create_all(self.engine, tables=[AnimeGenre.__table__])

    def create_producer_table(self):
        from .model import Base, Producer

        Base.metadata.create_all(self.engine, tables=[Producer.__table__])

    def create_tables(self):
        from .model import Base
        Base.metadata.create_all(self.engine)

    def load_producers(self, producers: Iterable[Dict] = None):
        if producers is None:
            raise ValueError('producers is None in load_producers()')

        from .model import Producer

        with Session(self.engine) as session:
            for p in producers:
                if not session.get(Producer, p['mal_id']):
                    i, n = p['mal_id'], p['titles'][0]['title']
                    session.add(Producer(id=i, name=n))
            session.commit()

    def load_genres(self, genres: Iterable[Dict] = None):
        if genres is None:
            raise ValueError('genres is None in load_genres()')

        from .model import Genre

        def not_exists(genre):
            if not session.get(Genre, genre['mal_id']):
                return True
            else:
                return False

        with Session(self.engine) as session:
            for g in filter(not_exists, genres):
                session.add(Genre(id=g['mal_id'], name=g['name']))
            session.commit()

    def load_anime(self, anime: Iterable[Dict] = None):
        if anime is None:
            raise ValueError('anime is None in load_anime()')

        from model import Anime

        with Session(self.engine) as session:
            keys = ('mal_id', 'title', 'title_english', 'episodes', 'type',
                    'source', 'season', 'year', 'rating', 'synopsis', 'score',
                    'members')

            for a in anime:
                d = {key: a[key] for key in keys}
                obj = Anime(**d)
                if not session.get(Anime, obj.mal_id):
                    try:
                        session.add(obj)
                    except SQLAlchemyError as error:
                        print('load_anime() ERROR with', d['mai_id'], error)

            session.commit()
