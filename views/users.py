from flask import render_template, request, redirect, url_for, g
from models import DBStorage
from views import dashboard


@dashboard.route('/<uuid:user_id>')
def user_profile(user_id):
    return render_template('dashboard.html', user_id=user_id)


@dashboard.route('/<uuid:user_id>/delete', methods=['GET', 'POST'])
def delete_user(user_id):
    if request.method == 'POST':
        print('method is delete')
        
        with DBStorage() as db:
            g.user_deletion = True
            user_id = str(user_id)
            db.handle_user(user_id=user_id, delete=True)
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('delete_user.html', user_id=user_id)
    
