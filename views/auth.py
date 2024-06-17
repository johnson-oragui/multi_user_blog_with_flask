from flask import request, redirect, render_template, url_for
from models import DBStorage
from views import authenticate
from forms.register_form import RegisterForm
from forms.login_form import LoginForm




@authenticate.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate():
            user_dict: dict = {
                'username': form.username.data,
                'first_name': form.first_name.data,
                'last_name': form.last_name.data,
                'email': form.email.data,
                'password': form.password.data
            }

            with DBStorage() as db:
                new_user = db.handle_user(user_dict)
            if isinstance(new_user, dict):
                return redirect(url_for('authenticate.login'))
            else:
                return render_template('register.html', form=form)
        else:
            print('form validated?: ', form.validate())
            return render_template('register.html', form=form)
    elif request.method == 'GET':
        return render_template('register.html', form=form)
    else:
        return f'method not allowed'
    
@authenticate.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            user_dict = {
                'username': form.username.data,
                'password': form.password.data
            }
            with DBStorage() as db:
                pass
        else:
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)