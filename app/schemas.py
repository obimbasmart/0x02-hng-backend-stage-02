from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    

class UserIn(UserBase):
    password: str

class UserInCreate(UserIn):
    firstName: str
    lastName: str
    phone: str
    
class UserOut(UserBase):
    userId: str = Field(alias='id')
    firstName: str
    lastName: str
    phone: str

    class Config:
        from_attributes = True

class UserCreateResponse:
    status: str
    message: str
    data: UserOut

class UserOrgAdd(BaseModel):
    id: str


class OrgBase(BaseModel):
    name: str

class OrgIn(OrgBase):
    description: Optional[str] = None

class OrgOut(OrgIn):
    orgId: str = Field(alias='id')

    class Config:
        from_attributes = True


