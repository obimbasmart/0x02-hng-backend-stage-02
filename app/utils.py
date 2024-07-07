from fastapi import HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
import bcrypt
from pydantic import ValidationError
from datetime import datetime, timedelta,timezone
from typing import Optional
from .config import get_settings
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from .database import get_db

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="accessToken")


def generate_password_hash(pwd: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=pwd.encode('utf-8'), salt=salt)


def verify_password(pwd: str, hashed_pwd: str):
    return bcrypt.checkpw(pwd.encode('utf-8'), bytes.fromhex(hashed_pwd[2:])) # adding slice due to postgress data handling


def authenticate_user(password: str, hashed_password: str):
    if not verify_password(password, hashed_password):
        return False
    return True

def generate_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    to_encode = data.copy()
    to_encode.update({"exp" : expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("userId")
        if not user_id:
            raise credential_exception
    except InvalidTokenError:
        raise credential_exception
    
    from .crude import get_user_by_id
    user = get_user_by_id(user_id, db)
    if not user:
        raise credential_exception
    
    return user


def format_validation_errors(exc: ValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": error["loc"][-1],  # Get the field name
            "message": error["msg"]
        })
    return {"errors": errors}