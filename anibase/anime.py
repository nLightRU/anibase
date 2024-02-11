import random

import flask_login
from flask import Blueprint, render_template, request
from flask import abort
from flask import current_app

from sqlalchemy import and_
from sqlalchemy.orm import Session

from .model import Anime, Genre, AnimeGenre, UserAnime
from .model import engine

anime = Blueprint('anime', __name__, url_prefix='/anime')


@anime.route('/')
def anime_all():
    with Session(engine) as session:
        page = request.args.get('page', 1, type=int)
        offset = page - 1
        per_page = current_app.config['PER_PAGE']
        pagination = session.query(Anime).order_by(Anime.members.desc()) \
                                          .slice(offset * per_page, offset*per_page + per_page)
    return render_template('anime_index.html', anime_titles=pagination, page=page)


@anime.route('/<int:id_>')
def anime_by_id(id_):
    with Session(engine) as session:
        try:
            anime_title = session.get(Anime, id_)
            if anime_title is None:
                abort(404)
            anime_genres = session.query(AnimeGenre).where(AnimeGenre.id_anime == id_).all()
            genres = []
            for ag in anime_genres:
                genres.append(session.get(Genre, ag.id_genre))
        except Exception as ex:
            print(ex)
            abort(404)

        user_info = dict()
        if flask_login.current_user.is_authenticated:
            user_info['user'] = flask_login.current_user
            ua = session.query(UserAnime).where(and_(user_info['user'].id == UserAnime.id_user,
                                                     UserAnime.id_anime == id_)).scalar()
            if ua:
                user_info['in_list'] = True
            else:
                user_info['in_list'] = False
        else:
            user_info['user'] = None

    return render_template('anime_id.html', anime=anime_title, genres=genres, user_info=user_info)


@anime.route('/year/<int:year_val>')
def anime_by_year(year_val):
    with Session(engine) as session:
        anime_titles = session.query(Anime).filter(Anime.year == year_val)
        anime_titles = sorted(anime_titles, key=lambda a: 0 if not a.score else a.score, reverse=True)
    return render_template('anime_year.html', titles=anime_titles, year=year_val)