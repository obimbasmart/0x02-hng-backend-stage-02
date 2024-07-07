from fastapi import APIRouter, Depends, status
from ..database import get_db
from ..crude import get_user_by_id
from .. import schemas
from ..utils import get_current_user
from fastapi.responses import JSONResponse
from ..models.user import User
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    # responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}")
def read_user(
    user_id: str,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)):

    user = get_user_by_id(user_id, db)
    if not user:
        return ({"error": "User does not exist"})
    
    current_user_organisations = [ org.id for org in current_user.organisations ]

    is_same_org = any([ org.id in current_user_organisations for org in user.organisations ])

    if not is_same_org:
        return JSONResponse({
            "status": "Unauthorized access",
            "message": "User not in same organisation"
        }, status.HTTP_401_UNAUTHORIZED)

    return ({
		"status": "success",
        "message": "User retrival successfull",
        "data": schemas.UserOut.model_validate(user).model_dump()
    }) 

