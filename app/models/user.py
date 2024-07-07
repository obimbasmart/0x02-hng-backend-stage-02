from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship
from .base_model import BaseModel, user_organisation
from ..utils import generate_password_hash, verify_password


class User(BaseModel):
    __tablename__ = "users"

    firstName = Column(String(60), nullable=False)
    lastName = Column(String(60), nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(String)

    organisations = relationship("Organisation", secondary=user_organisation, back_populates="users")

    def set_password(self, password: str):
        self.password = generate_password_hash(password)

    def check_password(self, password: str):
        return verify_password(self.password, password)
    
