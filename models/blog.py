from flask import g
import logging
from typing import List
from sqlalchemy import Integer, String, ForeignKey, event
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .base_model import Base, BaseModel


logger = logging.getLogger(__name__)

class Blog(BaseModel, Base):
    __tablename__ = 'blogs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(60), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title: Mapped[str] = mapped_column(String(60), nullable=False)
    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    category: Mapped[str] = mapped_column(String(60))

    comments: Mapped[List['Comment']] = relationship('Comment', backref='blog', cascade='all, delete-orphan')

def archive_blog(mapper, connection, target):
    '''Archive blog before deletion'''
    from .archived_blog import ArchivedBlog
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
            'user_id': target.user_id,
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