from sqlalchemy import Column, String, DateTime
# from sqlalchemy.orm import relationship
from .base_model import Base, BaseModel

class ArchivedUser(BaseModel, Base):
    __tablename__ = 'archived_users'

    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    username = Column(String(60), nullable=False, unique=True)
    email = Column(String(60), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    initial_created_at = Column(DateTime, nullable=False)
    initial_updated_at = Column(DateTime, nullable=False)
