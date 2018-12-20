from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
from . import subject
from .. import db
from ..decorators import admin_required
from ..models import Movie
import base64


@subject.route('/movies')
def movies():
    movies = Movie.query.order_by(Movie.name).all()
    return render_template('subject/movies.html', movies=movies)


@subject.route('/movie/<int:id>')
def movie(id):
    movie = Movie.query.get_or_404(id)
    return render_template('subject/movie.html', movie=movie)
