from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
from . import manage
from .forms import EditMovieForm, CreateMovieForm
from .. import db
from ..decorators import admin_required
from ..models import Movie
import base64


@manage.route('/manage-movies', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_movies():
    movies = Movie.query.order_by(Movie.name).all()
    return render_template('manage/manage_movies.html', movies=movies)


@manage.route('/edit-subject/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_movie(id):
    movie = Movie.query.get_or_404(id)
    form = EditMovieForm(movie)
    if form.validate_on_submit():
        if form.submit.data:
            movie.name = form.name.data
            movie.date = form.date.data
            movie.price = form.price.data
            if form.picture.data:
                movie.picture = request.files['picture'].read()
            movie.director = form.director.data
            movie.description = form.description.data
            db.session.add(movie)
            db.session.commit()
            flash('电影资料已更新')
        elif form.delete.data:
            db.session.delete(movie)
            db.session.commit()
            flash('电影资料已删除')
        return redirect(url_for('manage.manage_movies'))
    form.name.data = movie.name
    form.date.data = movie.date
    form.price.data = movie.price
    form.director.data = movie.director
    form.description.data = movie.description
    return render_template('manage/edit_movie.html', form=form, movie=movie)


@manage.route('/create-subject', methods=['GET', 'POST'])
@login_required
@admin_required
def create_movie():
    form = CreateMovieForm()
    movie = Movie()
    if form.validate_on_submit():
        if form.submit.data:
            movie.name = form.name.data
            movie.date = form.date.data
            movie.price = form.price.data
            if form.picture.data:
                movie.picture = request.files['picture'].read()
            movie.director = form.director.data
            movie.description = form.description.data
            db.session.add(movie)
            db.session.commit()
            flash('电影资料已创建')
            return redirect(url_for('manage.edit_movie', id=movie.id))
        else:
            return redirect(url_for('manage.manage_movies'))
    form.name.data = movie.name
    form.date.data = movie.date
    form.price.data = movie.price
    form.director.data = movie.director
    form.description.data = movie.description
    return render_template('manage/create_movie.html', form=form)
