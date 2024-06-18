from flask import g
import logging
from typing import List
from sqlalchemy import String, ForeignKey,Integer, event
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, BaseModel

logger = logging.getLogger(__name__)


class Comment(BaseModel, Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(60), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    blog_id: Mapped[str] = mapped_column(Integer, ForeignKey('blogs.id', ondelete='CASCADE'), nullable=False)
    comment: Mapped[str] = mapped_column(String(255))

# Ensure the @event.listens_for decorator is placed outside the class
# definition to correctly bind the event.
@event.listens_for(Comment, 'before_delete')
def archive_comment(mapper, connection, target):
    '''Archive comment before deletion'''
    from .archived_comment import ArchivedComment
    try:
        flag_value = getattr(g, 'user_deletion')
        print('flag_value from comment: ', flag_value)
        print()
        if flag_value:
            return
    except AttributeError:
        pass
    try:
        comment_to_archive = {
            'comment_id': target.id,
            'user_id': target.user_id,
            'blog_id': target.blog_id,
            'comment': target.comment,
            'initial_created_at': target.created_at,
            'initial_updated_at': target.updated_at,
            'is_from_account_deletion': False
        }
        print('now running hook for comment: ')
        connection.execute(ArchivedComment.__table__.insert().values(comment_to_archive))
    except Exception as exc:
        logger.error(f'error archiving comment before deletion: {exc}')
