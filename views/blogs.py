from flask import render_template, request, redirect, url_for, g
from models import DBStorage
from views import dashboard
from forms.blog_form import BlogForm


@dashboard.route('/<uuid:user_id>/blogs')
def blogs(user_id):
    my_blogs = None
    with DBStorage() as db:
        try:
            user_id = str(user_id)
        except TypeError:
            return render_template('blogs.html', my_blogs=my_blogs)
        my_blogs = db.get_blogs(user_id=user_id)
    return render_template('blogs.html', blogs=my_blogs, user_id=user_id)

@dashboard.route('/<uuid:user_id>/blog/<uuid:blog_id>')
def single_blog(user_id, blog_id):
    IDS = {
        'user_id': user_id,
        'blog_id': blog_id
    }
    with DBStorage() as db:
        pass
    return render_template('blogs.html', IDS=IDS)


@dashboard.route('/<uuid:user_id>/new_blog', methods=['GET', 'POST'])
def add_blog(user_id):
    form  = BlogForm(request.form)
    if request.method == 'POST':
        if form.validate():
            blog_dict = {
                'title': form.title.data,
                'content': form.content.data,
                'category': form.category.data,
                'user_id': str(user_id)
            }

            with DBStorage() as db:
                result = db.handle_blog(str(user_id), blog_dict)
                print('result: ', result)
            return redirect(url_for('dashboard.blogs', user_id=user_id))
        else:
            return render_template('new_blog.html', form=form, user_id=user_id)
    return render_template('new_blog.html', form=form, user_id=user_id)


@dashboard.route('/<uuid:user_id>/blog/<uuid:blog_id>/delete/', methods=['GET', 'POST'])
def delete_blog(user_id, blog_id):
    IDS = {
        'user_id': user_id,
        'blog_id': blog_id
    }
    
    form = BlogForm(request.form)
    if request.method == 'POST':
        g.user_deletion = False
        with DBStorage() as db:
            pass
        return redirect(url_for('dashboard.blogs', user_id=user_id))
    return render_template('delete_blog.html', form=form, IDS=IDS)
