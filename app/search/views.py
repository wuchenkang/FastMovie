from flask import render_template, request, current_app
from sqlalchemy import and_, or_, extract
from . import search
from ..models import Movie


@search.route('/')
def search():
    page = request.args.get('page', 1, type=int)
    name = request.args.get('name')
    director = request.args.get('director')
    year = request.args.get('year')

    sentence = True
    if name != '':
        sentence = and_(sentence, Movie.name.like('%' + name + '%'))

    if director != '':
        sentence = and_(sentence, Movie.director.like('%' + director + '%'))

    if year == '2019':
        sentence = and_(sentence, extract('year', Movie.date) == 2019)
    elif year == '2018':
        sentence = and_(sentence, extract('year', Movie.date) == 2018)
    elif year == '2017':
        sentence = and_(sentence, extract('year', Movie.date) == 2017)
    elif year == '2016-2011':
        sentence = and_(sentence, extract('year', Movie.date) <=2016)
        sentence = and_(sentence, extract('year', Movie.date) >= 2011)
    elif year == '2011-2000':
        sentence = and_(sentence, extract('year', Movie.date) <= 2010)
        sentence = and_(sentence, extract('year', Movie.date) >= 2001)
    elif year == '更早':
        sentence = and_(sentence, extract('year', Movie.date) <= 2000)

    result = Movie.query.filter(sentence)
    pagination = result.paginate(
        page, per_page=current_app.config['ITEM_PER_PAGE'],
        error_out=False
    )
    movies = pagination.items
    return render_template('search/search.html', movies=movies, name=name, director=director, year=year, pagination=pagination)
