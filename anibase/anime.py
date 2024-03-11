from flask import Blueprint, render_template, request, url_for
from flask import abort, redirect
from flask import current_app

from flask_login import login_required, current_user

from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from .model import Anime, Genre, AnimeGenre, User, UserAnime, Comment
from .model import engine

from .forms import CommentForm

anime = Blueprint('anime', __name__, url_prefix='/anime')


@anime.route('/')
def anime_all():
    context = {}
    with Session(engine) as session:
        page = request.args.get('page', 1, type=int)
        offset = page - 1
        per_page = current_app.config['PER_PAGE']
        anime_page = session.query(Anime).order_by(Anime.members.desc()) \
                                          .slice(offset * per_page, offset*per_page + per_page)

        pages_total = int(session.query(Anime).count() / current_app.config['PER_PAGE'])

        context['anime_titles'] = anime_page
        context['page'] = page

        context['pages_total'] = pages_total

        if page < 5:
            pages_numbers_show = [1, 2, 3, 4]
        elif page + 5 > pages_total:
            start = page - (page + 4 - pages_total)
            pages_numbers_show = [p for p in range(start, pages_total+1)]
        else:
            start = page - 5
            # +3 because range doesn't include last number
            end = page + 5
            pages_numbers_show = [p for p in range(start, end)]

        context['pages_numbers_show'] = tuple(pages_numbers_show)

    return render_template('anime_index.html', **context)


@anime.route('/<int:id_>')
def anime_by_id(id_):
    form = CommentForm()
    context = {}
    with Session(engine) as session:
        try:
            anime_title = session.get(Anime, id_)
            if anime_title is None:
                abort(404)
            else:
                context['anime'] = anime_title
            anime_genres = session.query(AnimeGenre).where(AnimeGenre.id_anime == id_).all()
            genres = []
            for ag in anime_genres:
                genres.append(session.get(Genre, ag.id_genre))
            context['genres'] = genres
        except Exception as ex:
            print(ex)
            abort(404)

        if current_user.is_authenticated:
            user = current_user
            ua = session.query(UserAnime).where(and_(user.id == UserAnime.id_user,
                                                     UserAnime.id_anime == id_)).scalar()
            if ua:
                context['in_list'] = True
            else:
                context['in_list'] = False

        comments_rows = session.execute(select(Comment.id_user, Comment.content).
                                        where(Comment.id_anime == id_),
                                        execution_options={"prebuffer_rows": True}).all()

        comments = []
        for comment in comments_rows:
            comments.append(
                {
                    'username': session.get(User, comment.id_user).username,
                    'content': comment.content
                }
            )

        context['comment_form'] = form
        context['comments'] = comments

    return render_template('anime_id.html', **context)


@anime.route('/<int:id_>/comments', methods=['POST'])
@login_required
def post_comment(id_):
    form = CommentForm()
    with Session(engine) as session:
        if form.validate_on_submit():
            comment = Comment(id_user=current_user.id, id_anime=id_, content=form.content.data)
            session.add(comment)
            session.commit()

    return redirect(url_for('anime.anime_by_id', id_=id_))


@anime.route('/year/<int:year_val>')
def anime_by_year(year_val):
    with Session(engine) as session:
        anime_titles = session.query(Anime).filter(Anime.year == year_val)
        anime_titles = sorted(anime_titles, key=lambda a: 0 if not a.score else a.score, reverse=True)
    return render_template('anime_year.html', titles=anime_titles, year=year_val)
