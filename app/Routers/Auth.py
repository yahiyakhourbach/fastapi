from fastapi import  Depends, status, Response, HTTPException, APIRouter
from sqlalchemy.orm import session
from ..Schemas import UserLogin
from ..database import get_db
from .. import models, oauth2
from ..utils import validate_password
router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login_user(user_credentials:UserLogin,db: session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    if not validate_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    token = oauth2.create_access_token({"user_id":user.id,"username":user.username})
    return {"token":token, "token_type":"bearer"}
