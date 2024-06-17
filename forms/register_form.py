from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     IntegerField,
                     SubmitField,
                     ValidationError,
                     )
from wtforms.validators import DataRequired, EqualTo, Email

# reusable custom validator
def length_check(form, field):
    if len(field.data) > 25:
        raise ValidationError(f'{field.data} must not be more than 25 characters')

# factory callable validator
def length(min=1, max=1, message=None):
    if not message:
        message = f'Must be between {min} and {max} characters long.'

    def _length(form, field):
        len_data = len(field.data)
        if len_data < min or len_data > max or len_data == 0:
            raise ValidationError(message)

    return _length

class RegisterForm(FlaskForm):
    first_name = StringField('first name', validators=[DataRequired(), length_check])
    last_name = StringField('last name', validators=[DataRequired(), length(min=3, max=25)])
    username = StringField('username', validators=[DataRequired(), length(min=3, max=25)])
    email = StringField('email', validators=[
        DataRequired(),
        Email(check_deliverability=True)]
        )
    age = IntegerField('Age')
    password = PasswordField('password', validators=[
        DataRequired(),
        EqualTo('confirm', message='password must match')]
        )
    confirm = PasswordField('confirm password')
    submit = SubmitField('Register')

    # inline-custom-validator
    def validate_age(form, field):
        if field.data and field.data < 14:
            raise ValidationError("We're sorry, you must be 13 or older to register")
    
    # inline-custom-validator
    def validate_password(form, field):
        if len(field.data) < 6:
            raise ValidationError('Password must be up to six characters long')
        not_allowed_pwd = ['123456', '1234567890', '0987654321', 'password']
        if field.data in not_allowed_pwd:
            raise ValidationError('C\'mon, is that what you could think of?')
