from typing import Iterable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class DBManager:
    def __init__(self, database, user, password):
        try:
            self.engine = create_engine(f'postgresql+psycopg2://{user}:{password}@localhost/{database}')
        except:
            print("Can't connect to database")

    def create_anime_table(self):
        from .model import Base, Anime

        Base.metadata.create_all(self.engine, tables=[Anime.__table__])

    def create_genre_table(self):
        from .model import Base, Genre

        Base.metadata.create_all(self.engine, tables=[Genre.__table__])

    def create_tables(self):
        from .model import Base
        Base.metadata.create_all(self.engine)

    def load_genres(self, genres: Iterable = None):
        if genres is None:
            raise ValueError('genres is None in load_genres()')

        from .model import Genre

        def not_exists(g):
            if not session.get(Genre, g['mal_id']):
                return True
            else:
                return False

        with Session(self.engine) as session:
            for g in filter(not_exists, genres):
                session.add(Genre(id=g['mal_id'], name=g['name']))
            session.commit()

    def load_anime(self, anime: Iterable = None):
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
                    except:
                        print('Error with', d['mai_id'])

            session.commit()


