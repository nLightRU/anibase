from flask import  Blueprint, render_template
from .model import db, Anime

anime = Blueprint('anime', __name__, url_prefix='/')


@anime.route('/anime/id/<int:mal_id>')
def anime_by_id(mal_id):
    anime = db.get_or_404(Anime, mal_id)
    return f"<h1>Anime</h1><ul><li>id: {anime.mal_id}</li><li>name: {anime.title}</li><li>year: {anime.year}</li></ul>"


@anime.route('/anime/year/<int:year_val>')
def anime_by_year(year_val):
    return f"<p>anime for year {year_val}</p>"

