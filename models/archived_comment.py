from datetime import datetime
from sqlalchemy import String, DateTime, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base
from .base_model_archive import BaseModelArchive



class ArchivedComment(BaseModelArchive, Base):
    __tablename__ = 'archived_comments'

    comment_id: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(String(255), nullable=False)
    blog_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[str] = mapped_column(String(60), nullable=False)
    initial_created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    initial_updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_from_account_deletion: Mapped[bool] = mapped_column(Boolean, default=True)
