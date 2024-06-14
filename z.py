import time
from models import DBStorage
from models.user import User
from models.blog import Blog
from models.comment import Comment
from models.archived_user import ArchivedUser
from models.archived_blog import ArchivedBlog
from models.archived_comment import ArchivedComment


with DBStorage() as db:
    
    db.drop_all_tables()
    time.sleep(3)
    db.create_all_tables()

# f_name = 'Johnson1'
# l_name = 'Dennis'
# username = 'Johnson1'
# email = 'email1@email.com'
# password = 'johnson'

# user = User(
#     first_name=f_name,
#     last_name=l_name,
#     username=username,
#     email=email,
#     password=password
#     )

# comment = Comment(
#     comment='This is a comment',
#     )
# user.comments.append(comment)
# db.add(user)
# db.add(comment)

# db.save()

# print(db.delete_user('2befef89-f5af-4dd7-a28e-d28504510b59'))
