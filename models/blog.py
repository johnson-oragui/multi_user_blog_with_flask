from flask import g
import logging
from sqlalchemy import Column, Boolean, String, ForeignKey, event
from sqlalchemy.orm import relationship
from .base_model import Base, BaseModel
from .archived_blog import ArchivedBlog

logger = logging.getLogger(__name__)

class Blog(BaseModel, Base):
    __tablename__ = 'blogs'

    user_id = Column(String(60), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(60), nullable=False)
    content = Column(String(1000), nullable=False)
    is_from_account_deletion = Column(Boolean, default=True)
    user = relationship('User', back_populates='blogs')
    comments = relationship('Comment', back_populates='blog', cascade='all, delete-orphan')

def archive_blog(mapper, connection, target):
    '''Archive blog before deletion'''
    try:
        flag_value = getattr(g, 'user_deletion')
        print('flag_value from blog: ', flag_value)
        if flag_value:
            return
    except AttributeError:
        pass
    try:
        blog_to_archive = {
            'id': target.id,
            'user_id': target.id,
            'title': target.title,
            'content': target.content,
            'initial_created_at': target.created_at,
            'initial_updated_at': target.updated_at,
            'is_from_account_deletion': False
        }
        connection.execute(ArchivedBlog.insert().values(blog_to_archive))
    except Exception as exc:
        logger.error(f'error archiving blog before deletion: {exc}')

event.listen(Blog, 'before_delete', archive_blog)