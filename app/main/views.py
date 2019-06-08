import base64
from flask import render_template, redirect, url_for, request
from flask_login import current_user
from sqlalchemy import and_
from .. import db
from ..models import Movie, Trolley
from . import main


@main.route('/')
def index():
    movies = Movie.query.order_by(Movie.total_score / Movie.total_rating).limit(6).all()
    return render_template('index.html', movies=movies, num=len(movies), range=range, base64=base64, round=round)


@main.route('/', methods=['post'])
def trolley():
    old_items = Trolley.query.filter(and_(Trolley.user_id == current_user.id, Trolley.inTrolley == True)).all()
    for i in range(len(request.form)):
        args = request.form[str(i)].split('|')
        inTrolley = False
        new_item = None
        for old_item in old_items:
            if old_item.movie_id == args[0]:
                inTrolley = True
                new_item = old_item
                break
        if not inTrolley:
            new_item = Trolley()
        new_item.user_id = int(current_user.id)
        new_item.movie_id = int(args[0])
        new_item.movie_name = args[1]
        new_item.movie_price = float(args[2])
        new_item.movie_count = int(args[3])
        new_item.multiply_commodities = True
        movie = Movie.query.filter(Movie.id == int(args[0])).first()
        new_item.movie = movie
        db.session.add(new_item)
    for old_items in old_items:
        stillIn = False
        for i in range(len(request.form)):
            if old_items.movie_id == request.form[str(i)].split('|')[0]:
                stillIn = True
        if not stillIn:
            db.session.delete(old_items)
    db.session.commit()
    return redirect(url_for('main.index'))
