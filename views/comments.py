from flask import render_template, request, redirect, url_for, g
from models import DBStorage
from views import dashboard
from forms.comment_form import CommentForm




@dashboard.route('/<uuid:user_id>/blog/<int:blog_id>/new_comment', methods=['GET', 'POST'])
def new_comment(user_id, blog_id):
    form = CommentForm(request.form)
    IDS = {
        'user_id': user_id,
        'blog_id': blog_id
    }
    if request.method == 'POST':
        if form.validate():
            comment = form.comment.data

            with DBStorage() as db:
                db.handle_comment(user_id, comment, blog_id)
                pass
            return redirect(url_for('dashboard.blog', user_id=user_id, blog_id=blog_id))
        else:
            return render_template('new_comment.html', form=form, IDS=IDS)
    return render_template('new_comment.html', form=form, IDS=IDS)


@dashboard.route('/<uuid:user_id>/blog/<int:blog_id>/comment/<int:comment_id>/delete', methods=['GET', 'POST'])
def delete_comment(user_id, blog_id, comment_id):
    form = CommentForm(request.form)
    IDS = {
        'user_id': user_id,
        'blog_id': blog_id,
        'comment_id': comment_id
    }
    if request.method == 'POST' and request.form.get('_method') == 'DELETE':
        g.user_deletion = False
        with DBStorage() as db:
            pass
        return redirect(url_for('dashboard.blog', user_id=user_id, blog_id=blog_id))
    return render_template('delete_comment.html', form=form, IDS=IDS)