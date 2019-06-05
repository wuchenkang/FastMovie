import base64
from flask import render_template
from ..models import  Movie
from . import main


@main.route('/')
def index():
    movies = Movie.query.order_by(Movie.total_score / Movie.total_rating).limit(6).all()
    return render_template('index.html', movies=movies, num=len(movies), range=range, base64=base64, )
