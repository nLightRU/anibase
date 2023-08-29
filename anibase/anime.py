from flask import Blueprint, render_template
from .model import db, Anime

anime = Blueprint('anime', __name__, url_prefix='/')


@anime.route('/anime/id/<int:mal_id>')
def anime_by_id(mal_id):
    anime_title = db.get_or_404(Anime, mal_id)
    return render_template('anime.html', anime=anime_title)


@anime.route('/anime/year/<int:year_val>')
def anime_by_year(year_val):
    anime_titles = db.session.query(Anime).filter(Anime.year == year_val)
    return render_template('anime_year.html', titles=anime_titles, year=year_val)
