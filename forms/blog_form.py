from flask_wtf import FlaskForm
from wtforms import (StringField, ValidationError, SubmitField, TextAreaField)
from wtforms.validators import DataRequired

class BlogForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    category = StringField('category')
    submit = SubmitField('add blog')

    def validate_title(form, field):
        if len(field.data) > 60:
            raise ValidationError('Title must not be more than 60 characters')

    def validate_content(form, field):
        if len(field.data) > 1000:
            raise ValidationError('Blog length must not be more than a though characters')