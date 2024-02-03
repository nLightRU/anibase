from typing import Sequence


from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class DBManager:
    def __init__(self, database, user, password):
        self.engine = create_engine(f'postgresql+psycopg2://{user}:{password}@localhost/{database}')

    def create_anime_table(self):
        from model import Base, Anime

        Base.metadata.create_all(self.engine, tables=[Anime.__table__])

    def create_tables(self):
        from model import Base
        Base.metadata.create_all(self.engine)

    def load_anime(self, anime: Sequence):
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


