from flask import g
import logging
from uuid import uuid4
from sqlalchemy import Column, String, event
from sqlalchemy.orm import relationship
from .base_model import Base, BaseModel
from .archived_blog import ArchivedBlog
from .archived_user import ArchivedUser
from .archived_comment import ArchivedComment

logger = logging.getLogger(__name__)


class User(BaseModel, Base):
    __tablename__ = 'users'

    id = Column(String(60), primary_key=True, default=str(uuid4()))
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    username = Column(String(60), nullable=False, unique=True)
    email = Column(String(60), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    blogs = relationship('Blog',
                            back_populates='user',
                            cascade='all, delete-orphan')
    comments = relationship('Comment',
                            back_populates='user',
                            cascade='all, delete-orphan')


def handle_user_deletion(mapper, connection, target):
    '''Archive user before deletion'''
    try:
        flag_value = getattr(g, 'user_deletion')
        print('flag_value from user: ', flag_value)
        print()
        if not flag_value:
            print('flag is false for user deletion, returning...')
            return
    except AttributeError:
        pass
    print('hook running now for user deletion: ')

    # check for blogs associated with the user
    if target.blogs:
        # if blogs, iterate through the blogs
        for blog in target.blogs:
            # create a dict of the blog
            blog_to_archive = {
                'blog_id': blog.id,
                'title': blog.title,
                'content': blog.content,
                'category': blog.category,
                'user_id': blog.user_id,
                'initial_created_at': blog.created_at,
                'initial_updated_at': blog.updated_at,
            }
            # check for comments associated with the blog
            if blog.comments:
                # if comments found, iterate through the comments
                for comment in blog.comments:
                    # create a dict of the comments
                    comments_to_archive = {
                        'comment_id': comment.id,
                        'blog_id': comment.blog_id,
                        'comment': comment.comment,
                        'user_id': comment.user_id,
                        'initial_updated_at': comment.updated_at,
                        'initial_created_at': comment.created_at
                    }
                    try:
                        # archive comments
                        connection.execute(ArchivedComment.__table__.insert().values(comments_to_archive))
                    except Exception as exc:
                        logger.error(f'error with archiving comments at User model: {exc}')
            try:
                # archive blogs
                connection.execute(ArchivedBlog.__table__.insert().values(blog_to_archive))
            except Exception as exc:
                logger.error(f'error archiving blogs at User model {exc}')
            

    # create a dict of the user to archive
    user_to_archive = {
        'user_id': target.id,
        'first_name': target.first_name,
        'last_name': target.last_name,
        'username': target.username,
        'email': target.email,
        'password': target.password,
        'initial_created_at': target.created_at,
        'initial_updated_at': target.updated_at
    }
    try:
        # archive the user before delete
        connection.execute(ArchivedUser.__table__.insert().values(user_to_archive))
    except Exception as exc:
        logger.error(f'error archiving user at Useer model: {exc}')
    

event.listen(User, 'before_delete', handle_user_deletion)
