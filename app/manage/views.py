from flask import render_template
from . import manage
from ..decorators import admin_required
from ..models import Movie


@manage.route('/edit-movie/<int:id>')
@admin_required
def edit_movie(id):
    movie = Movie.query.get_or_404(id)
    pass
