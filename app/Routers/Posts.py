from fastapi import  status, HTTPException,Response,Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import  get_db
from .. import models
from ..Schemas import Post, TokenData, PostLikes,PostResponse,UserResponse
from ..oauth2 import get_current_data
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/",response_model=List[PostLikes])
def home(db:Session = Depends(get_db), userData :TokenData = Depends(get_current_data)):

    query = db.query(models.Post,func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Post.id ==models.Vote.post_id, isouter=True).group_by(models.Post.id).all()
    response = [{"Posts": post, "likes": likes} for post, likes in query]
    return response

@router.post("/",status_code=status.HTTP_201_CREATED)
def createposts(post: Post,db:Session = Depends(get_db),userData :TokenData = Depends(get_current_data)):
    
    new_post =  models.Post(owner_id = userData.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"created" : new_post}

@router.get("/{id}", response_model = PostLikes)
def get_post(id:str,db: Session = Depends(get_db), userData :TokenData = Depends(get_current_data)):
    try:
        id = int(id)
        query  = db.query(models.Post,func.count(models.Vote.post_id).label("likes")).join(models.Vote,models.Post.id == models.Vote.post_id, isouter=True).filter(models.Post.id == id).group_by(models.Post.id).first()
        
        if not query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id : {id} was not found")
        _post, likes = query
        post = PostResponse.from_orm(_post)
        return PostLikes(Posts=post, likes=likes)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"invalid id : {id}")

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:str,db: Session = Depends(get_db), userData :TokenData = Depends(get_current_data)):
    try:
        id = int(id)
        post = db.query(models.Post).filter(models.Post.id == id )
        _post = post.first()

        if not _post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id : {id} was not found")
        if _post.owner_id != userData.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"forbidden action")

        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"invalid id : {id}")

@router.put("/{id}")
def update_post(id:str, post:Post,db:Session = Depends(get_db), userData :TokenData = Depends(get_current_data)):
    try:
        id = int(id)
        updated_post = db.query(models.Post).filter(models.Post.id == id)
        _post = updated_post.first()

        if not _post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id : {id} was not found")
        if _post.owner_id != userData.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"forbidden action")

        updated_post.update(post.dict(),synchronize_session=False)
        db.commit()
        return {"updated_post":updated_post.first()}

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"invalid id : {id}")

