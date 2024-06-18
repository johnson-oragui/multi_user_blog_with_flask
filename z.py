# import time
# from models.db_engine.db_storage import DBStorage
# from app import flask_app, g


# f_name = 'Prince'
# l_name = 'Dennis'
# username = 'Prince'
# email = 'Prince@email.com'
# password = 'Prince'

# user_dict = {
#     'first_name': f_name,
#     'last_name': l_name,
#     'username': username,
#     'email': email,
#     'password': password,
#     'preferences': {'theme': 'dark', 'language': 'en'}
# }

# title = 'title 1'
# content = 'first blog'
# category = 'None'

# blog_dict = {
#     'title': title,
#     'content': content,
#     'category': category
# }

# comment = 'This is a comment'

# app = flask_app()

# user_updates = {
#             'first_name': 'new fname',
#             'last_name': 'new lastname',
# }
# blog_updates = {
#     'title': 'Updated Title',
#     'content': 'Updated Content',
# }
# comment_updates = 'Updated Comment'

# with app.app_context():
#     with DBStorage() as db:
#         g.user_deletion = True
    
#         db.drop_all_tables()
#         time.sleep(2)
#         db.create_all_tables()
#         time.sleep(2)

#         print()
#         print()


#         new_user = db.handle_user(user_dict=user_dict)

#         print()

#         new_blog = db.handle_blog(user_id=new_user.get('id') , blog_dict=blog_dict)

#         print()

#         new_comment = db.handle_comment(user_id=new_user.get('id'), blog_id=new_blog.get('id'), comment=comment)

        # print()

        # time.sleep(2)
        # print()
        # print()

        # Update user
        # updated_user = db.handle_user(user_id=new_user['id'], user_dict=user_updates, edit=True)
        # print(f'Updated User: {updated_user}')

        # # Update blog
        # updated_blog = db.handle_blog(user_id=new_user['id'], blog_id=1, blog_dict=blog_updates, edit=True)
        # print(f'Updated Blog: {updated_blog}')

        # # Update comment
        # updated_comment = db.handle_comment(user_id=new_user['id'], blog_id=new_blog['id'], comment_id=new_comment['id'], comment=comment_updates, edit=True)
        # print(f'Updated Comment: {updated_comment}')

        # time.sleep(2)

        # print()
        # print()

        # comment_to_del = db.handle_comment(user_id=new_user['id'], blog_id=new_blog['id'], comment_id=new_comment['id'], delete=True)
        # print('comment_to_del: ', comment_to_del)
        
        # blog_to_del = db.handle_blog(user_id=new_user['id'], blog_id=new_blog['id'], delete=True)
        # print('blog_to_del: ', blog_to_del)

        # user_to_del = db.handle_user(user_id=new_user['id'], delete=True)
        # print('user_to_del: ', user_to_del)
