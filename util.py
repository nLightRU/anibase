import time
from datetime import datetime

from anibase import jikan
from anibase.dbmanager import DBManager


if __name__ == '__main__':
    db_manager = DBManager(user='anibase_admin', password='1234', database='anibase')
    i = 0
    for a in db_manager.get_all_anime():
        if i == 5:
            break

        url = jikan.get_anime(a.mal_id)['images']['jpg']['image_url']
        if url is None:
            continue

        db_manager.add_image_url(a.mal_id, url)
        print(a.mal_id, url)
        i += 1

    # db_manager.create_user_follow_table()

    # db_manager.load_genres(jikan.get_genres())

    # print(a)
    # for year in range(2015, 2022):
    #     anime = jikan.get_season('summer', year, type_='tv')
    #     print(year)
    #     time.sleep(2)
    #     db_manager.load_anime(anime, has_genres=True, has_prods=True)






