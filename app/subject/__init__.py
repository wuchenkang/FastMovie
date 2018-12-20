from flask import Blueprint

subject = Blueprint('subject', __name__)

from . import views
