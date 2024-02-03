from typing import Sequence

import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class DataLoader:
    api = 'https://api.jikan.moe/v4'

    def __init__(self):
        self.engine = create_engine('postgresql+psycopg2://anibase_admin:1234@localhost/anibase')
        self.api_url = 'https://api.jikan.moe/v4'

    def get_season_now(self, type_=None) -> tuple:
        """
            Returns a tuple of dictionaries
        """
        p = {'filter': None, 'page': 1}
        if type_ is None:
            p['filter'] = 'tv'
        elif type_ in ('movie', 'ova', 'special', 'ona', 'music'):
            p['filter'] = type_
        else:
            raise ValueError(f'No such type "{type_}" in anime database')
                
        url = f'{self.api_url}/seasons/now'
        resp_body = requests.get(url, params=p).json()
        print(url)
        # print(resp_body)

        data = resp_body['data']

        while resp_body['pagination']['has_next_page']:
            p['page'] += 1
            resp_body = requests.get(url, params=p).json()
            data.extend(resp_body['data'])

        return tuple(data)

    def create_anime_table(self):
        from model import Base, Anime

        Base.metadata.create_all(self.engine, tables=[Anime.__table__])

    def create_tables(self):
        from model import Base
        Base.metadata.create_all(self.engine)

    def load_anime(self, anime: Sequence):
        from model import Anime
        from sqlalchemy import insert

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


if __name__ == '__main__':
    # now = DataLoader.get_season_now(type_='movie')
    loader = DataLoader()
    # loader.create_anime_table()
    titles = loader.get_season_now()
    loader.load_anime(titles)


