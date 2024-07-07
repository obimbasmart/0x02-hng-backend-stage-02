from sqlalchemy import Column, String, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
import uuid

from ..database import Base


# Association table for many-to-many relationship
user_organisation = Table('user_organisation', Base.metadata,
    Column('user_id', String, ForeignKey('users.id')),
    Column('org_id', String, ForeignKey('organisations.id'))
)


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(String(60), primary_key=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(tz='UTC'))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(tz='UTC'),
                                                 onupdate=func.now(tz='UTC'))
    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
        self.id = uuid.uuid4().hex