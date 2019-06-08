from flask import render_template, request, current_app
from flask_login import login_required, current_user
from . import trolley
from ..models import Trolley


@trolley.route('/')
@login_required
def view_trolley():
    page = request.args.get('page', 1, type=int)
    pagination = Trolley.query.filter(Trolley.user_id==current_user.id).order_by(Trolley.movie_name).paginate(
        page, per_page=current_app.config['ITEM_PER_PAGE'],
        error_out=False
    )
    items = pagination.items
    return render_template('trolley/trolley.html', items=items, pagination=pagination)


@trolley.route('/submit', methods=['post'])
@login_required
def submit():
    return "successful!"
