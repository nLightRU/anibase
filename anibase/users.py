from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from sqlalchemy import and_
from sqlalchemy.orm import Session
from .model import engine, UserAnime


users = Blueprint('users', __name__, url_prefix='/')


@users.route('/user/<int:id_user>')
def user(id_user):
    return f"<p>user {id_user}</p>"


@users.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@users.route('/add-anime', methods=['POST'])
def add_anime():
    id_anime = int(request.form.get('anime_id'))
    with Session(engine) as session:
        ua = session.query(UserAnime).where(and_(current_user.id == UserAnime.id_user,
                                                 UserAnime.id_anime == id_anime)).scalar()
        if not ua:
            session.add(UserAnime(id_user=current_user.id, id_anime=id_anime))
            session.commit()
    return redirect(url_for('views.anime_by_id', id_=id_anime))
