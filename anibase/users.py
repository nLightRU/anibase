from flask import Blueprint, render_template, redirect, url_for, request, abort, make_response
from flask_login import login_required, current_user

from sqlalchemy import and_, select
from sqlalchemy.orm import Session, Bundle
from anibase import db
from .model import engine, User, UserAnime, Anime, UserFollow

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/')
def users_list():
    with Session(engine) as session:
        users_ = session.query(User).all()
    return render_template('users_list.html', users=users_)


@users.route('/<username>')
@login_required
def user_by_username(username):
    with Session(engine) as session:
        context = {}

        u = session.query(User).where(User.username == username).first()
        user_id = u.id
        if u:
            context['user'] = u
        else:
            abort(404)
        user_anime_ids = session.execute(select(UserAnime.id_anime).
                                         where(UserAnime.id_user == user_id)).scalars()
        user_anime = session.query(Anime).where(Anime.mal_id.in_(user_anime_ids)).limit(20)
        context['user_anime'] = user_anime

        context['following'] = db.user_followings(u)

        if u.id != current_user.id:
            is_follow = session.query(UserFollow.id_user_follow).where(and_(UserFollow.id_user == current_user.id,
                                                                            UserFollow.id_user_follow == u.id)).scalar()
            print(is_follow)
            if is_follow:
                context['is_follow'] = True
            else:
                context['is_follow'] = False

    return render_template('user.html', **context)


@users.route('/<username>/animelist', methods=['GET'])
def user_animelist(username):
    with Session(engine) as session:
        context = {}

        u = session.query(User).where(User.username == username).first()
        if u:
            context['user'] = u
        else:
            abort(404)

        stmt = select(Bundle("anime", Anime.mal_id, Anime.title, Anime.image_url),
                      Bundle("status", UserAnime.status)).join(UserAnime.user_anime).where(UserAnime.id_user == u.id)

        user_list = []
        animelist_rows = session.execute(stmt).all()

        for a in animelist_rows:
            user_list.append(
                {
                    "mal_id": a[0][0],
                    "title": a[0][1],
                    "image_url": a[0][2],
                    "status": a[1][0]
                }
            )

        context['user_anime'] = user_list

    return render_template('user_animelist.html', **context)


@users.route('/<username>/animelist', methods=['POST'])
@login_required
def add_anime(username):
    id_anime = request.get_json().get('anime_id')
    with Session(engine) as session:
        ua = session.query(UserAnime).where(and_(current_user.id == UserAnime.id_user,
                                                 UserAnime.id_anime == id_anime)).scalar()
        if not ua:
            session.add(UserAnime(id_user=current_user.id, id_anime=id_anime))
            session.commit()
    return make_response('', 200)


@users.route('/<username>/animelist', methods=['PATCH'])
@login_required
def remove_anime(username):
    data = request.get_json()
    id_anime = data.get('anime_id')

    with Session(engine) as session:
        ua = session.query(UserAnime).where(and_(current_user.id == UserAnime.id_user,
                                                 UserAnime.id_anime == id_anime)).scalar()
        if not ua:
            abort(500)
        else:
            session.delete(ua)
            session.commit()

    return make_response('', 200)


@users.route('<username>/following', methods=['PATCH'])
@login_required
def follow_user(username):
    data = request.get_json()

    follow_id = data.get('follow_id')
    action = data.get('action')

    with Session(engine) as session:
        uf = session.query(UserFollow).where(and_(UserFollow.id_user == current_user.id,
                                                  UserFollow.id_user_follow == follow_id)
                                             ).first()
        if action == 'follow':
            session.add(UserFollow(id_user=current_user.id, id_user_follow=follow_id))
            session.commit()
        elif action == 'unfollow':
            session.delete(uf)
            session.commit()
        else:
            abort(500)

    return make_response('', 200)
