
from sqlalchemy import Column, String, DateTime, Boolean, Integer
# from sqlalchemy.orm import relationship
from .base_model import Base
from .base_model_archive import BaseModelArchive



class ArchivedComment(BaseModelArchive, Base):
    __tablename__ = 'archived_comments'

    comment_id = Column(Integer, nullable=False)
    comment = Column(String(255), nullable=False)
    blog_id = Column(String(60), nullable=False)
    user_id = Column(String(60), nullable=False)
    initial_created_at = Column(DateTime, nullable=False)
    initial_updated_at = Column(DateTime, nullable=False)
    is_from_account_deletion = Column(Boolean, default=True)
