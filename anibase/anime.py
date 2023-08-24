from flask import  Blueprint, render_template

anime = Blueprint('anime', __name__, url_prefix='/')


@anime.route('/anime/id/<int:mal_id>')
def anime_by_id(mal_id):
    return f"<h1>Anime</h1><ul><li>name: Anime</li><li>year: 2007</li><li>id: {mal_id}</li></ul>"


@anime.route('/anime/year/<int:year_val>')
def anime_by_year(year_val):
    return f"<p>anime for year {year_val}</p>"

