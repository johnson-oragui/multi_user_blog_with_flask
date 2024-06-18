from views import admin
from models import DBStorage


@admin.route('/admin/<uuid:admin_id>')
def admin_dashboard(admin_id):
    pass


@admin.route('/admin/<uuid:admin_id>')
def all_users(admin_id):
    pass


@admin.route('/admin/<uuid:admin_id>/user/<uuid:user_id>')
def block_user(admin_id, user_id):
    pass


@admin.route('/admin/<uuid:admin_id>/delete/<uuid:user_id>', methods=['GET', 'POST'])
def delete_user(admin_id, user_id):
    pass



@admin.route('/admin/<uuid:admin_id>/blogs')
def all_blogs(admin_id):
    pass


@admin.route('/admin/<uuid:admin_id>/blog/<int:blog_id>', methods=['GET', 'POST'])
def delete_blog(admin_id, blog_id):
    pass

@admin.route('/admin/<uuid:admin_id>/comments')
def all_comments(admin_id):
    pass


@admin.route('/admin/<uuid:admin_id>/comment/<int:comment_id>', methods=['GET', 'POST'])
def delete_comment(admin_id, comment_id):
    pass