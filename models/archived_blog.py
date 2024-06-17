from sqlalchemy import Column, String, DateTime, Boolean, Integer
from .base_model import Base
from .base_model_archive import BaseModelArchive


class ArchivedBlog(BaseModelArchive, Base):
    __tablename__ = 'archived_blogs'

    blog_id = Column(Integer)
    user_id = Column(String(60), nullable=False)
    title = Column(String(60), nullable=False)
    content = Column(String(1000), nullable=False)
    category = Column(String(60))
    initial_created_at = Column(DateTime)
    initial_updated_at = Column(DateTime)
    is_from_account_deletion = Column(Boolean, default=True)

    # def __init__(self, **kwargs) -> None:
    #     super(ArchivedBlog, self).__init__(**kwargs)
    #     self.archived_user_id = kwargs.get('user_id')
    
    # comments = relationship('Comment', backref='blogs', cascade='all')