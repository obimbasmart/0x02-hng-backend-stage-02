from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from ..utils import get_current_user
from ..crude import get_user_by_id, get_org_by_id, create_org
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas

router = APIRouter(
    prefix="/api/organisations",
    tags=["Organisation"],
    # responses={404: {"description": "Not found"}},
)

@router.get("/")
def get_organisations(current_user: schemas.UserOut = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    user = get_user_by_id(current_user.id, db)
    return JSONResponse({
                "status": "success",
                "message": "<message>",
                "data": {
                "organisations": [
                    schemas.OrgOut.model_validate(org).model_dump()
                    for org in user.organisations
                ]
        }
    })

@router.post("/")
def create_organisation(org: schemas.OrgIn,
                        current_user: schemas.UserOut = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    
    new_org = create_org(org, db)
    current_user.organisations.append(new_org)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return JSONResponse({
        "status": "success",
        "message": "Organisation created successfully",
        "data": schemas.OrgOut.model_validate(new_org).model_dump()
    }, status.HTTP_201_CREATED)
    
    

@router.get("/{org_id}")
async def read_user(org_id: str, db=Depends(get_db),
                    current_user: schemas.UserOut = Depends(get_current_user)):
    
    if org_id not in [org.id for org in current_user.organisations]:
        return JSONResponse({
            "status": "Not Found",
            "message": "No organisation found"
        }, status.HTTP_404_NOT_FOUND)
    
    org = get_org_by_id(org_id, db)
    return JSONResponse({
        "status": "success",
        "message": "Organisation retrieval successfull",
        "data": schemas.OrgOut.model_validate(org).model_dump()
    })


@router.post("/{org_id}/users")
async def add_user_to_organisation(org_id: str,
                                   _user: schemas.UserOrgAdd, db=Depends(get_db)):
    org = get_org_by_id(org_id, db)
    if not org:
        return JSONResponse({
            "status": "Not Found",
            "message": "No organisation found"
        }, status.HTTP_404_NOT_FOUND)
    
    user = get_user_by_id(_user.id, db)
    if not user:
        return JSONResponse({
            "status": "Not Found",
            "message": "No user record found"
        }, status.HTTP_404_NOT_FOUND)
    
    user.organisations.append(org)
    db.add(user)
    db.commit()
    db.refresh(user)
    return JSONResponse({
        "status": "success",
        "message": "User added to organisation successfully",
    }, status.HTTP_200_OK)
    
