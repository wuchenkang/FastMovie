from flask import render_template, redirect, request, url_for, flash, current_app
from flask_login import login_required
from . import manage
from .forms import EditMovieForm, CreateMovieForm
from .. import db
from ..decorators import admin_required
from ..models import Movie, Comment
import base64


@manage.route('/manage-movies', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_movies():
    page = request.args.get('page', 1, type=int)
    pagination = Movie.query.order_by(Movie.name).paginate(
        page, per_page=current_app.config['ITEM_PER_PAGE'],
        error_out=False
    )
    movies = pagination.items
    return render_template('manage/manage_movies.html', movies=movies, pagination=pagination)


@manage.route('/edit-movie/<int:id>', methods=['GET', 'POST'])
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
            comments = Comment.query.filter(Comment.movie_id==id).all()
            for comment in comments:
                db.session.delete(comment)
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


@manage.route('/create-movie', methods=['GET', 'POST'])
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
