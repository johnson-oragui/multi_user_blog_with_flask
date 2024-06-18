from datetime import datetime
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import mapped_column, Mapped
from .base_model import Base
from .base_model_archive import BaseModelArchive

class ArchivedUser(BaseModelArchive, Base):
    __tablename__ = 'archived_users'

    user_id: Mapped[int] = mapped_column(String(60), nullable=False)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    username: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(60), nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    initial_created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    initial_updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
