from anibase import jikan
from anibase.dbmanager import DBManager


if __name__ == '__main__':
    db_manager = DBManager(user='anibase_loader', password='1234', database='anibase')
    titles = jikan.get_season(now=True)
    data = jikan.get_genres()
    print(data)




