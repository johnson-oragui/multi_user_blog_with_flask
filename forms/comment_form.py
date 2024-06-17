from flask_wtf import FlaskForm
from wtforms import TextAreaField, ValidationError, SubmitField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    comment = TextAreaField('comment', validators=[DataRequired()])
    submit = SubmitField('comment')

    def validate_comment(form, field):
        if len(form.data) > 60:
            raise ValidationError('Comment must not be more than 60 characters')