from flask_wtf import FlaskForm
from wtforms import StringField, DateField, DecimalField, FileField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Movie

class EditMovieForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired()])
    data = DateField('上映日期')
    price = DecimalField('价格', places=2)
    picture = FileField('上传海报')
    director = StringField('导演', 64)
    description = TextAreaField('简介')
    submit = SubmitField('提交')
