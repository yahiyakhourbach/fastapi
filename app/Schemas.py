from pydantic import BaseModel, EmailStr
from  datetime import datetime


class Post(BaseModel):
    title:str
    content:str

class User(BaseModel):
    username:str
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    username:str
    email:EmailStr

    class Config:
        from_attributes = True


class PostResponse(Post):
    id          : int
    title       :str
    content     :str
    user        : UserResponse
    created_at  : datetime

    class Config:
        from_attributes = True

class PostLikes(BaseModel):
    Posts   :PostResponse
    likes   :int

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    token: str
    type: str

class TokenData(BaseModel):
    id: int
    username:str

class Votes(BaseModel):
    post_id :int
    vote_dir :int

