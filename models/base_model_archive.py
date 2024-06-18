from datetime import datetime
from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import mapped_column, Mapped


class BaseModelArchive:
    archive_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
