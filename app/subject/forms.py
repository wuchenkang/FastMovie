from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class CreateCommentForm(FlaskForm):
    title = TextAreaField('标题', validators=[DataRequired(), Length(1, 32)], render_kw={'rows': '1'})
    comment = TextAreaField('评论', validators=[DataRequired(), Length(1, 512)])
    submit = SubmitField('提交', render_kw={'id': 'submit'})

    def __init__(self, *args, **kwargs):
        super(CreateCommentForm, self).__init__(*args, **kwargs)
