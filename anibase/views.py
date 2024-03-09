import random

from flask import Blueprint, render_template, request, abort
from flask import current_app

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from .model import Anime, Producer
from .model import engine
from anibase import db


views = Blueprint('views', __name__, url_prefix='/')


@views.route('/')
def index():
    year = random.randint(2015, 2020)
    a = db.select_top_year(year)
    return render_template('index.html', anime=a)


@views.route('/producers')
def studios():
    with Session(engine) as session:
        page = request.args.get('page', 1, type=int)
        offset = page - 1
        per_page = current_app.config['PER_PAGE']
        pagination = session.query(Producer).slice(offset * per_page,
                                                 offset*per_page + per_page)
    return render_template('producers.html', studios=pagination, page=page)


@views.route('/seasons')
def seasons():
    context = {
        'seasons': db.select_seasons()
    }

    return render_template('seasons_index.html', **context)


@views.route('/seasons/<season>/<int:year>')
def season(season, year):
    if season not in ('winter', 'spring', 'summer', 'fall'):
        abort(404)

    context = {
        'season': season,
        'year': year
    }

    with Session(db.engine) as session:
        anime = session.query(Anime).where(and_(Anime.season == season, Anime.year == year)).all()
        context['anime'] = anime

    return render_template('season.html', **context)