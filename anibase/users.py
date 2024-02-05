from flask import Blueprint, render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user

from sqlalchemy import and_, select
from sqlalchemy.orm import Session
from .model import engine, User, UserAnime, Anime, UserFollow

users = Blueprint('users', __name__, url_prefix='/')


@users.route('/users')
def users_list():
    with Session(engine) as session:
        users_ = session.query(User).all()
    return render_template('users_list.html', users=users_)


@users.route('/users/<int:user_id>')
@login_required
def user_by_id(user_id):
    user_info = dict()
    with Session(engine) as session:
        u = session.get(User, user_id)
        if u:
            user_info['user'] = u
        else:
            abort(404)
        user_anime_ids = session.execute(select(UserAnime.id_anime).
                                         where(UserAnime.id_user == user_id)).scalars()
        user_anime = session.query(Anime).where(Anime.mal_id.in_(user_anime_ids)).limit(20)
        user_info['user_anime'] = user_anime

        if u.id != current_user.id:
            is_follow = session.query(UserFollow).where(and_(UserFollow.id_user == current_user.id,
                                                             UserFollow.id_user_follow == u.id)).scalar()
            if is_follow:
                user_info['is_follow'] = True
            else:
                user_info['is_follow'] = False

    return render_template('user.html', user_info=user_info)


@users.route('/users/<username>')
def user_by_username(username):
    with Session(engine) as session:
        u_id = session.query(User.id).where(User.username == username).scalar()
        if u_id:
            return redirect(url_for('users.user_by_id', user_id=u_id))
        else:
            abort(404)


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
