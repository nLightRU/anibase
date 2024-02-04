import time
from datetime import datetime

from anibase import jikan
from anibase.dbmanager import DBManager


if __name__ == '__main__':
    db_manager = DBManager(user='anibase_admin', password='1234', database='anibase')
    # titles = jikan.get_season(now=True)
    # genres = jikan.get_genres()
    db_manager.create_anime_table()
    # db_manager.load_genres(genres)
    # db_manager.create_producer_table()

    # write anime loading from 1970 to now

    seasons = ('winter', 'spring', 'summer', 'fall')
    types = ('tv', 'movie', 'ova', 'ona')
    with open('log.txt', 'w', encoding='utf-8') as log:
        for y in range(1980, 2024):
            for s in seasons:
                for t in types:
                    data = []
                    data.extend(jikan.get_season(s, y, type_=t))
                    db_manager.load_anime(data)
                    time.sleep(2)
                print(y, s)
                log.write(f'{y}, {s}, {len(data)}\n')
        # db_manager.load_anime(data)






