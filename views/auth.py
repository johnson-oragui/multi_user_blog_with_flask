from flask import request, redirect, render_template, url_for
from models import DBStorage
from views import authenticate
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from utils.auth_manager import AuthManager




@authenticate.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate():
            # generate token to complete registration
            token = AuthManager.generate_jwt_token(email=form.email.data, registration=True)
            user_dict: dict = {
                'username': form.username.data,
                'first_name': form.first_name.data,
                'last_name': form.last_name.data,
                'email': form.email.data,
                'password': form.password.data,
                'reg_token': token
            }

            with DBStorage() as db:
                new_user = db.handle_user_insertion(user_dict)
            if isinstance(new_user, dict):
                # send token to user's email with registration confirmation link
                AuthManager.create_confirmation_link(user_dict.get('email'), token)

                # redirect to login page
                return redirect(url_for('authenticate.login', username=new_user.get('username')))
            else:
                return render_template('register.html', form=form)
        else:
            print('form validated?: ', form.validate())
            return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)


@authenticate.route('/confirm/<string:token>')
def complete_registration(token):
    # validate token
    email = AuthManager.verify_jwt_token(token=token, registration=True)
    if email == 'expired' or email == 'invalid':
        print(f'token expired or invalid: {token}')
        return render_template('invalid_token.html')
    user_dict = {
        'email': email,
        'reg_token': token,
    }
    # activate user account by setting is_active to True
    with DBStorage() as db:
        # validate and process token, return True if token is valid
        update_user = db.handle_user_update(user_dict=user_dict, update=True)
    if update_user:
        return redirect(url_for('authenticate.login', username=update_user.get('username')))
    return redirect(url_for('authenticate.login'))


@authenticate.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.args.get('username'):
        form.username.data = request.args.get('username')
    if request.method == 'POST':
        if form.validate():
            user_dict = {
                'username': form.username.data,
                'password': form.password.data
            }
            with DBStorage() as db:
                found_user = db.handle_user_login(user_dict=user_dict, login=True)
                if found_user and found_user.get('is_active'):
                    # generate token
                    AuthManager.generate_jwt_token(username=found_user.get('username'),
                                                   user_id=found_user.get('id'),
                                                   login=True)
                else:
                    # flash message incorrect username or password
                    return render_template('login.html', form=form)
        else:
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@authenticate.get('/test')
@AuthManager.login_required
def test_():
    print(request.headers.get('token'))
    return f'working right'