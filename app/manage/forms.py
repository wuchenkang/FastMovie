from flask_wtf import FlaskForm
from wtforms import StringField, DateField, DecimalField, FileField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class EditMovieForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired()])
    date = DateField('上映日期')
    price = DecimalField('价格', rounding=2)
    picture = FileField('上传海报')
    director = StringField('导演')
    description = TextAreaField('简介')
    submit = SubmitField('提交')
