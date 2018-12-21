from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, DateField, DecimalField, FileField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class CreateCommentForm(FlaskForm):
    title = TextAreaField('标题', validators=[DataRequired(), Length(1, 32)], render_kw={'rows': '1'})
    comment = TextAreaField('评论', validators=[DataRequired(), Length(1, 256)])
    submit = SubmitField('提交')
    back = SubmitField('返回', render_kw={
        'onclick': "javascript:history.back(1);"})

    def __init__(self, *args, **kwargs):
        super(CreateCommentForm, self).__init__(*args, **kwargs)
