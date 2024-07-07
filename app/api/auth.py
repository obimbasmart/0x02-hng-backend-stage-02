from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..crude import create_user, get_user_by_email
from .. import schemas
from ..utils import authenticate_user, generate_access_token
from ..database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    # responses={404: {"description": "Not found"}},
)

@router.post("/register")
def register(user: schemas.UserInCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(user.email, db)
    if db_user:
        return JSONResponse({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 400
    }, status.HTTP_400_BAD_REQUEST)
    
    new_user = create_user(user, db)
    return JSONResponse({
                "status": "success",
                "message": "Registration successful",
                "data": {
                    "accessToken": generate_access_token({"userId": new_user.id}),
                    "user": schemas.UserOut.model_validate(new_user).model_dump()
                }
            }, status_code=status.HTTP_201_CREATED)



@router.post("/login")
def login(user: schemas.UserIn, db: Session = Depends(get_db)):
    db_user = get_user_by_email(user.email, db)
    if db_user and authenticate_user(user.password, db_user.password):
        return ({
            "status": "success",
            "message": "Login successful",
            "data": {
            "accessToken": generate_access_token({'userId' : db_user.id}),
            "user": schemas.UserOut.model_validate(db_user).model_dump()
            }
        })
    return JSONResponse({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
            }, status.HTTP_401_UNAUTHORIZED)

# Add more user-related routes...