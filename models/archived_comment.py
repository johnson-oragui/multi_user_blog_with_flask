
from sqlalchemy import Column, String, DateTime, Boolean
# from sqlalchemy.orm import relationship
from .base_model import Base, BaseModel

class ArchivedComment(BaseModel, Base):
    __tablename__ = 'archived_comments'

    comment = Column(String(255))
    blog_id = Column(String(60), nullable=False)
    user_id = Column(String(60), nullable=False)
    initial_created_at = Column(DateTime, nullable=False)
    initial_updated_at = Column(DateTime, nullable=False)
    is_from_account_deletion = Column(Boolean, default=True)