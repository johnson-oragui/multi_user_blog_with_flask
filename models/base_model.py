from datetime import datetime
from sqlalchemy import MetaData, DateTime, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.declarative import declared_attr

# Naming Convention for Constraints
naming_convention = {
    "pk": "pkey_%(table_name)s_%(column_0_name)s",
    "fk": "fkey_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "ix": "index_%(table_name)s_%(column_0_name)s",
    "uq": "unique_%(table_name)s_%(column_0_name)s",
    "ck": "constraint_%(table_name)s_%(constraint_name)s"
}

# Metadata Object with Naming Convention
my_metadata = MetaData(naming_convention=naming_convention)

# Base Class with Metadata
class Base(DeclarativeBase):
    metadata = my_metadata

    @declared_attr
    def __tablename__(cls):
        table_name = cls.__name__.lower()
        return f'{table_name}s'

# Mixin class
class BaseModel:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

# Automatically update updated_at field before update
@event.listens_for(Base, 'before_update', propagate=True)
def receive_before_update(mapper, connection, target):
    target.updated_at = datetime.now()