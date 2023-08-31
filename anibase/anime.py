from flask import Blueprint, render_template
from flask import abort
from sqlalchemy import select
from sqlalchemy.orm import Session

from .model import Anime, Genre, AnimeGenre
from .model import engine

anime = Blueprint('anime', __name__, url_prefix='/')


@anime.route('/anime/id/<int:mal_id>')
def anime_by_id(mal_id):
    genres = []
    with Session(engine) as session:
        try:
            anime_title = session.get(Anime, mal_id)
            anime_genres = session.execute(select(AnimeGenre).where(AnimeGenre.id_anime == mal_id))
            for ag in anime_genres.scalars():
                genres.append(session.get(Genre, ag.id_genre))
        except Exception as ex:
            print(ex)
            abort(404)

    return render_template('anime.html', anime=anime_title, genres=genres)


@anime.route('/anime/year/<int:year_val>')
def anime_by_year(year_val):
    with Session(engine) as session:
        anime_titles = session.query(Anime).filter(Anime.year == year_val)
        anime_titles = sorted(anime_titles, key=lambda a: 0 if not a.score else a.score, reverse=True)
    return render_template('anime_year.html', titles=anime_titles, year=year_val)
