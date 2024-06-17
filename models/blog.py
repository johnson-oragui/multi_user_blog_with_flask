from flask import g
import logging
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, event
from sqlalchemy.orm import relationship
from .base_model import Base, BaseModel
from .archived_blog import ArchivedBlog

logger = logging.getLogger(__name__)

class Blog(BaseModel, Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(60), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(60), nullable=False)
    content = Column(String(1000), nullable=False)
    category = Column(String(60))
    is_from_account_deletion = Column(Boolean, default=True)
    user = relationship('User', back_populates='blogs')
    comments = relationship('Comment', back_populates='blog', cascade='all, delete-orphan')

def archive_blog(mapper, connection, target):
    '''Archive blog before deletion'''
    try:
        flag_value = getattr(g, 'user_deletion')
        print('flag_value from blog: ', flag_value)
        print()
        if flag_value:
            return
    except AttributeError:
        pass
    try:
        blog_to_archive = {
            'blog_id': target.id,
            'user_id': target.id,
            'title': target.title,
            'content': target.content,
            'category': target.category,
            'initial_created_at': target.created_at,
            'initial_updated_at': target.updated_at,
            'is_from_account_deletion': False
        }
        print('now running hook for blog: ')
        connection.execute(ArchivedBlog.__table__.insert().values(blog_to_archive))
    except Exception as exc:
        logger.error(f'error archiving blog before deletion: {exc}')

event.listen(Blog, 'before_delete', archive_blog)