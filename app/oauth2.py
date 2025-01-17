from jose import JWTError ,jwt
from datetime import datetime, timedelta
from .Schemas import TokenData
from fastapi import Depends, HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from .Config import settings


oauth_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM  = settings.algorithm
ACCESS_TOKEN_EXPIRATION_TIME = settings.token_expiration


def create_access_token(data:dict):

    to_encode   = data.copy()
    expiration  = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_TIME)
    to_encode.update({"exp":expiration})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def validate_access_token(token:str, credentials_exception):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        username = payload.get("username")

        if id is None or username is None:
            raise credentials_exception
        token_data = TokenData(id = id, username = username)

    except JWTError:
        raise credentials_exception
    return token_data

def get_current_data(token:str = Depends(oauth_schema)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail=f"Could not validate credentials",
                                        headers={"www-Authenticate":"Bearer"})
    return validate_access_token(token=token, credentials_exception=credentials_exception)
    
