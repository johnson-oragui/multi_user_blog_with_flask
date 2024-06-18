from datetime import datetime
from sqlalchemy import String, DateTime, Boolean, Integer
from sqlalchemy.orm import mapped_column, Mapped
from .base_model import Base
from .base_model_archive import BaseModelArchive


class ArchivedBlog(BaseModelArchive, Base):
    __tablename__ = 'archived_blogs'

    blog_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[str] = mapped_column(String(60), nullable=False)
    title: Mapped[str] = mapped_column(String(60), nullable=False)
    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    category: Mapped[str] = mapped_column(String(60))
    initial_created_at: Mapped[datetime] = mapped_column(DateTime)
    initial_updated_at: Mapped[datetime] = mapped_column(DateTime)
    is_from_account_deletion: Mapped[bool] = mapped_column(Boolean, default=True)
