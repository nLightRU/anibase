from typing import Optional
import os

from sqlalchemy import create_engine, URL
from sqlalchemy import Integer, Float, String, Text, Sequence
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import mapped_column

from flask_login import UserMixin


from werkzeug.security import generate_password_hash, check_password_hash


db_url = URL.create(
    'postgresql+psycopg2',
    username=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME')
)

engine = create_engine(db_url)
Base = declarative_base()


class Anime(Base):
    __tablename__ = 'anime'

    mal_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    title_english: Mapped[Optional[str]] = mapped_column(String)
    episodes: Mapped[Optional[int]] = mapped_column(Integer)
    type: Mapped[Optional[str]] = mapped_column(String)
    source: Mapped[Optional[str]] = mapped_column(String)
    season: Mapped[Optional[str]] = mapped_column(String)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    rating: Mapped[Optional[str]] = mapped_column(String)
    synopsis: Mapped[Optional[str]] = mapped_column(Text)
    score: Mapped[Optional[float]] = mapped_column(Float)
    members: Mapped[Optional[int]] = mapped_column(Integer, default=0)


class Genre(Base):
    __tablename__ = 'genre'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return f'<Genre id={self.id} name={self.name}>'


class Producer(Base):
    __tablename__ = 'producer'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return f'<Studio id={self.id} name={self.name}>'


class AnimeGenre(Base):
    __tablename__ = 'anime_genre'
    id: Mapped[int] = mapped_column(Integer, Sequence('ag_id', start=1), primary_key=True)
    id_anime: Mapped[int] = mapped_column(ForeignKey('anime.mal_id'))
    id_genre: Mapped[int] = mapped_column(ForeignKey('genre.id'))

    def __repr__(self):
        return f'<AnimeGenre id={self.id} id_anime={self.id_anime} id_genre={self.id_genre}>'


class AnimeProducer(Base):
    __tablename__ = 'anime_producer'
    id: Mapped[int] = mapped_column(Integer, Sequence('ap_id', start=1), primary_key=True)
    id_anime: Mapped[int] = mapped_column(ForeignKey('anime.mal_id'))
    id_producer: Mapped[int] = mapped_column(ForeignKey('producer.id'))


class User(UserMixin, Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[int] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String(128))
    # registration_date: Mapped[date] = mapped_column(Date, default=func.current_date())

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserAnime(Base):
    __tablename__ = 'user_anime'
    id: Mapped[int] = mapped_column(Integer, Sequence('ua_id', start=1), primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey('user.id'))
    id_anime: Mapped[int] = mapped_column(ForeignKey('anime.mal_id'))


class UserFollow(Base):
    __tablename__ = 'user_follow'
    id_user: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_user_follow: Mapped[int] = mapped_column(Integer, primary_key=True)
