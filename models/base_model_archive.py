from datetime import datetime
from sqlalchemy import Column, Integer, DateTime


class BaseModelArchive:
    archive_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
