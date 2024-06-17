from sqlalchemy import Column, String, DateTime, Integer
from .base_model import Base
from .base_model_archive import BaseModelArchive

class ArchivedUser(BaseModelArchive, Base):
    __tablename__ = 'archived_users'

    user_id = Column(String(60), nullable=False)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    username = Column(String(60), nullable=False, unique=True)
    email = Column(String(60), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    initial_created_at = Column(DateTime, nullable=False)
    initial_updated_at = Column(DateTime, nullable=False)
