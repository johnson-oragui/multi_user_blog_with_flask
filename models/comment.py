from flask import g
import logging
from sqlalchemy import Column, String, ForeignKey, Boolean, event
from sqlalchemy.orm import relationship
from .base_model import Base, BaseModel
from .archived_comment import ArchivedComment

logger = logging.getLogger(__name__)


class Comment(BaseModel, Base):
    __tablename__ = 'comments'

    user_id = Column(String(60), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    blog_id = Column(String(60), ForeignKey('blogs.id', ondelete='CASCADE'), nullable=False)
    comment = Column(String(255))
    user = relationship('User', back_populates='comments')
    blog = relationship('Blog', back_populates='comments')
    is_from_account_deletion = Column(Boolean, default=True)

# Ensure the @event.listens_for decorator is placed outside the class
# definition to correctly bind the event.
@event.listens_for(Comment, 'before_delete')
def archive_comment(mapper, connection, target):
    '''Archive comment before deletion'''
    try:
        flag_value = getattr(g, 'user_deletion')
        print('flag_value from comment: ', flag_value)
        if flag_value:
            return
    except AttributeError:
        pass
    try:
        comment_to_archive = {
            'id': target.id,
            'user_id': target.user_id,
            'blog_id': target.blog_id,
            'comment': target.comment,
            'initial_created_at': target.created_at,
            'initial_updated_at': target.updated_at,
            'is_from_account_deletion': False
        }
        connection.execucomment_to_te(ArchivedComment.insert().values(comment_to_archive))
    except Exception as exc:
        logger.error(f'error archiving comment before deletion: {exc}')
