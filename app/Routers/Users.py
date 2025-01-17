from fastapi import  status, HTTPException,Response,Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db
from .. import models
from ..Schemas import User, UserResponse
from ..utils import hash_password
router = APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post("/",response_model=UserResponse)
def create_user(user:User,db:Session = Depends(get_db)):

    user.password = hash_password(user.password)
    created_user = models.User(**user.dict())
    _user = db.query(models.User).filter(models.User.username == user.username).first()
    if _user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"data already exist")
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user

