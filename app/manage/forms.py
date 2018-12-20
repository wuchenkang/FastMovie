from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, DateField, DecimalField, FileField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from wtforms import ValidationError
from ..models import Movie


class EditMovieForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired()])
    date = DateField('上映日期')
    price = DecimalField('价格', rounding=2)
    picture = FileField('海报', validators=[FileAllowed(['jpg', 'png'])])
    director = StringField('导演')
    description = TextAreaField('简介')
    submit = SubmitField('提交')
    delete = SubmitField('删除')

    def __init__(self, movie, *args, **kwargs):
        super(EditMovieForm, self).__init__(*args, **kwargs)
        self.movie = movie

    def validate_name(self, field):
        if field.data != self.movie.name and \
                Movie.query.filter_by(name=field.data).first():
            raise ValidationError('该电影名称已被使用！')


class CreateMovieForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired()])
    date = DateField('上映日期')
    price = DecimalField('价格', rounding=2)
    picture = FileField('海报', validators=[FileAllowed(['jpg', 'png'])])
    director = StringField('导演')
    description = TextAreaField('简介')
    submit = SubmitField('提交')

    def validate_name(self, field):
        if Movie.query.filter_by(name=field.data).first():
            raise ValidationError('该电影名称已被使用！')
