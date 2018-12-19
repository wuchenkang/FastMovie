from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
from . import manage
from .forms import EditMovieForm
from .. import db
from ..decorators import admin_required
from ..models import Movie


@manage.route('/edit-movie/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_movie(id):
    movie = Movie.query.get_or_404(id)
    form = EditMovieForm()
    if form.validate_on_submit():
        movie.name = form.name.data
        movie.date = form.date.data
        movie.price = form.price.data
        if request.files['picture'] is not None:
            movie.picture = request.files['picture'].read()
        movie.director = form.director.data
        movie.description = form.description.data
        db.session.add(movie)
        db.session.commit()
        flash('电影资料已更新')
        return redirect(url_for('main.index'))
    form.name.data = movie.name
    form.date.data = movie.date
    form.price.data = movie.price
    form.director.data = movie.director
    form.description.data = movie.description
    return render_template('manage/edit_movie.html', form=form, movie=movie)
