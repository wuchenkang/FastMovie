import base64
from flask import render_template, redirect, url_for, request
from flask_login import current_user
from .. import db
from ..models import Movie, Trolley
from . import main


@main.route('/')
def index():
    movies = Movie.query.order_by(Movie.total_score / Movie.total_rating).limit(6).all()
    return render_template('index.html', movies=movies, num=len(movies), range=range, base64=base64, round=round)


@main.route('/', methods=['post'])
def trolley():
    old_items = Trolley.query.filter(Trolley.user_id==current_user.id).all()
    for item in old_items:
        db.session.delete(item)
    for i in range(len(request.form)):
        new_item = Trolley()
        args = request.form[str(i)].split('|')
        new_item.user_id = int(current_user.id)
        new_item.movie_id = int(args[0])
        new_item.movie_name = args[1]
        new_item.movie_price = float(args[2])
        new_item.movie_count = int(args[3])
        new_item.multiply_commodities = True
        movie = Movie.query.filter(Movie.id == int(args[0])).first()
        new_item.movie = movie
        db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('main.index'))
