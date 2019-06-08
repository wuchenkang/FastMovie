from flask import current_app
from flask_login import current_user
from sqlalchemy import and_
from .models import Trolley


def get_trolley():
    trolley = Trolley.query.filter(and_(Trolley.user_id==current_user.id, Trolley.inTrolley==True)).order_by(Trolley.movie_id).all()
    return trolley
