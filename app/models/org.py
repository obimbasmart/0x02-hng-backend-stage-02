from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .base_model import BaseModel, user_organisation


class Organisation(BaseModel):
    __tablename__ = "organisations"

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    users = relationship("User", secondary=user_organisation, back_populates="organisations")
