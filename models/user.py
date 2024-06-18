from flask import g
import logging
from uuid import uuid4
from email_validator import validate_email, EmailNotValidError, EmailUndeliverableError
from typing import List
from sqlalchemy import String, Boolean, event
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from .base_model import Base, BaseModel
from .blog import Blog
from .comment import Comment
from .custom_type import ThemeAndLanguage
from .archived_blog import ArchivedBlog
from .archived_user import ArchivedUser
from .archived_comment import ArchivedComment


logger = logging.getLogger(__name__)


class User(BaseModel, Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(String(60), primary_key=True, default=lambda: str(uuid4()))
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    username: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    reg_token: Mapped[str] = mapped_column(String(35))
    preferences: Mapped[dict] = mapped_column(ThemeAndLanguage, default={'theme': 'light', 'language': 'en'})

    blogs: Mapped[List[Blog]] = relationship(backref='user', cascade='all, delete-orphan')
    comments: Mapped[List['Comment']] = relationship(backref='user', cascade='all, delete-orphan')
    # blogs: Mapped[List['Blog']] = relationship('Blog', backref='user', cascade='all, delete-orphan')
    # comments: Mapped[List['Comment']] = relationship('Comment', backref='user', cascade='all, delete-orphan')

    def __str__(self):
        user_data = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "blogs": self.blogs,
            "comments": self.comments,
        }
        return f'{{ {", ".join(f"{k}: {v}" for k, v in user_data.items())} }}'
    
    @validates('is_admin')
    def validate_is_admin(self, key, is_admin):
        '''prevents unauthorized modifications'''
        if key:
            raise ValueError(f'cannot set {is_admin}')
        if is_admin:
            raise ValueError(f'cannot set {is_admin}')
    
    @validates('email')
    def validate_email(self, key, address):
        try:
            is_valid = validate_email(address, check_deliverability=True)
            normalized_email = is_valid.normalized
            print('email validated: ', is_valid)
            return normalized_email
        except EmailUndeliverableError as exc:
            logger.error(f'an exception occured during email validation {exc}')
        except EmailNotValidError as exc:
            logger.error(f'email is invalid: {exc}')
        except ValueError as exc:
            logger.error(f'an exception occured during email validation {exc}')
        

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

    if target.is_admin:
        return

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
