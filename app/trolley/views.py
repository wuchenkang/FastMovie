from flask import render_template, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import and_, or_
from . import trolley
from ..models import Trolley
from .. import db


@trolley.route('/')
@login_required
def view_trolley():
    page = request.args.get('page', 1, type=int)
    pagination = Trolley.query.filter(Trolley.user_id==current_user.id).order_by(Trolley.movie_id).paginate(
        page, per_page=current_app.config['ITEM_PER_PAGE'],
        error_out=False
    )
    items = pagination.items
    return render_template('trolley/trolley.html', items=items, pagination=pagination)


@trolley.route('/add/<int:id>-<string:name>-<float:price>')
def add_trolley(id, name, price):
    if len(Trolley.query.filter(and_(Trolley.user_id==current_user.id, Trolley.movie_id == id)).all()) == 0:
        new_item = Trolley()
        new_item.user_id = current_user.id
        new_item.movie_id = id
        new_item.movie_name = name.strip()
        new_item.movie_price = price
        new_item.movie_count = 1
        db.session.add(new_item)
    else:
        old_item = Trolley.query.filter(and_(Trolley.user_id == current_user.id, Trolley.movie_id == id)).first()
        old_item.movie_count += 1
        db.session.add(old_item)
    db.session.commit()
    return redirect(url_for('trolley.view_trolley'))


@trolley.route('/submit', methods=['post'])
@login_required
def submit():
    return "successful!"
