from sqlalchemy.orm import Session
from fastapi import Depends

from . import schemas

from .models.user import User
from .models.org import Organisation
from .database import get_db


def create_user(user: schemas.UserInCreate, db: Session):
    new_user = User(firstName=user.firstName, lastName=user.lastName,
                    email=user.email, phone=user.phone)
    new_user.set_password(user.password)

    organisation_name = new_user.firstName + "'s Organisation"
    org = Organisation(name=organisation_name)
    new_user.organisations = [org]
    db.add_all([new_user, org])
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(id: str, db: Session):
    return db.query(User).filter(User.id == id).first()

def get_org_by_id(id: str, db: Session):
    return db.query(Organisation).filter(Organisation.id == id).first()

def create_org(org: schemas.OrgIn, db: Session):
    new_org = Organisation(name=org.name, description=org.description)
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org