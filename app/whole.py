from flask import current_app
from flask_login import current_user
from .models import Trolley


def get_trolley():
    trolley = Trolley.query.filter(Trolley.user_id==current_user.id).order_by(Trolley.movie_id).all()
    return trolley
