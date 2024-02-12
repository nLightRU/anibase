import random

from flask import Blueprint, render_template, request
from flask import current_app

from sqlalchemy.orm import Session

from .model import Producer
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
