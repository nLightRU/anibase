from typing import Iterable, Dict, Tuple

from sqlalchemy import Engine, create_engine, select, update, desc, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from .model import (Base, Anime, Genre, Producer, AnimeGenre, AnimeProducer,
                    User, UserAnime, UserFollow)


class DBManager:
    def __init__(self, url=None, database=None, user=None, password=None):
        try:
            if url is not None:
                self.engine = create_engine(url)
            else:
                self.engine = create_engine(f'postgresql+psycopg2://{user}:{password}@localhost/{database}')
        except SQLAlchemyError as error:
            print(f'DBManager init caused an error {error}')

    def create_anime_table(self):
        Base.metadata.create_all(self.engine, tables=[Anime.__table__])

    def create_genre_table(self):
        from .model import Base, Genre

        Base.metadata.create_all(self.engine, tables=[Genre.__table__])

    def create_producer_table(self):
        from .model import Base, Producer

        Base.metadata.create_all(self.engine, tables=[Producer.__table__])

    def create_anime_genre_table(self):
        Base.metadata.create_all(self.engine, tables=[AnimeGenre.__table__])

    def create_anime_producer_table(self):
        Base.metadata.create_all(self.engine, tables=[AnimeProducer.__table__])

    def create_user_table(self):
        Base.metadata.create_all(self.engine, tables=[User.__table__])

    def create_user_anime_table(self):
        Base.metadata.create_all(self.engine, tables=[UserAnime.__table__])

    def create_user_follow_table(self):
        Base.metadata.create_all(self.engine, tables=[UserFollow.__table__])

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def load_producers(self, producers: Iterable[Dict] = None):
        if producers is None:
            raise ValueError('producers is None in load_producers()')

        with Session(self.engine) as session:
            for p in producers:
                if not session.get(Producer, p['mal_id']):
                    i, n = p['mal_id'], p['titles'][0]['title']
                    session.add(Producer(id=i, name=n))
            session.commit()

    def load_genres(self, genres: Iterable[Dict] = None):
        if genres is None:
            raise ValueError('genres is None in load_genres()')

        def not_exists(genre):
            if not session.get(Genre, genre['mal_id']):
                return True
            else:
                return False

        with Session(self.engine) as session:
            # filter not existing genres for preventing adding twice
            for g in filter(not_exists, genres):
                session.add(Genre(id=g['mal_id'], name=g['name']))
            session.commit()

    def load_anime(self, anime: Iterable[Dict] = None, has_genres=False, has_prods=False):
        if anime is None:
            raise ValueError('anime is None in load_anime()')

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
                        print('load_anime() ERROR with', d['mal_id'], error)

                if has_genres:
                    if 'genres' in a.keys():
                        genres = a['genres']
                    if 'themes' in a.keys():
                        genres.extend(a['themes'])
                    for g in genres:
                        a_g = AnimeGenre(id_anime=a['mal_id'], id_genre=g['mal_id'])
                        if session.query(AnimeGenre).where(and_(AnimeGenre.id_anime == a_g.id_anime, AnimeGenre.id_genre == a_g.id_genre)).scalar():
                            continue
                        else:
                            session.add(a_g)

                if has_prods:
                    if 'studios' in a.keys():
                        studios = a['studios']
                        for s in studios:
                            a_s = AnimeProducer(id_anime=a['mal_id'], id_producer=s['mal_id'])
                            exists = session.query(AnimeProducer).where(and_(
                                                                    AnimeProducer.id_anime == a_s.id_anime,
                                                                    AnimeProducer.id_producer == a_s.id_producer)).scalar()
                            if not exists:
                                session.add(a_s)

            session.commit()

    def anime(self, id_):
        with Session(self.engine) as session:
            try:
                anime = session.get(Anime, id_)
                return anime
            except NoResultFound:
                print(f"No anime with id {id_}")
                return None

    def get_all_anime(self):
        with Session(self.engine) as session:
            anime = session.execute(select(Anime), execution_options={"prebuffer_rows": True}).scalars()
            for a in anime:
                yield a

    def select_top_year(self, year):
        with Session(self.engine) as session:
            stmt = select(Anime).where(Anime.year == year, Anime.score > 5, Anime.type == 'TV'
                                       ).order_by(desc(Anime.score)).limit(10)
            return session.scalars(stmt).all()

    def user_followings(self, user: User) -> tuple[User]:
        with Session(self.engine) as session:
            stmt = select(UserFollow.id_user_follow).where(UserFollow.id_user == user.id)
            follow_ids = session.execute(stmt).scalars()
            stmt = select(User).where(User.id.in_(follow_ids))
            followings = tuple(session.execute(stmt).scalars())

        return followings

    def add_image_url(self, anime_id: int = None, url: str = None):
        if anime_id is None:
            raise ValueError("Missing required arg 'anime_id'")
        if url is None:
            raise ValueError("Missing required arg 'url'")
        with Session(self.engine) as session:
            stmt = (update(Anime).
                    where(Anime.mal_id == anime_id).
                    values(image_url=url)
                    )
            session.execute(stmt)
            session.commit()

    def select_seasons(self) -> Tuple[Dict]:
        res = []
        with Session(self.engine) as session:
            seasons = session.execute(select(Anime.season).distinct()).scalars().all()
            for s in seasons:
                years = session.execute(select(Anime.year).where(Anime.season == s).distinct()).scalars().all()
                res.extend([{'season': s, 'year': y} for y in years])

        return tuple(res)
