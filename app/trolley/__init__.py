from flask import Blueprint

trolley = Blueprint('trolley', __name__)

from . import views
