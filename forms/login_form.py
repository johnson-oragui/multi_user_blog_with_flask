from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def validate_password(form, field):
        if len(field.data) < 6:
            raise ValidationError('password has to be upto six characters')