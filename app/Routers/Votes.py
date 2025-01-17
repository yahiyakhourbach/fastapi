from fastapi import APIRouter, Depends, HTTPException, status, Response
from ..database import get_db
from sqlalchemy.orm import Session
from ..oauth2 import get_current_data
from ..Schemas import Votes, TokenData
from ..models import Post,Vote
router = APIRouter(
    tags=["Votes"],
    prefix="/votes"
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_vote(vote:Votes,db: Session = Depends(get_db),user:TokenData = Depends(get_current_data)):
    try:
        query = db.query(Post).filter(Post.id == vote.post_id)
        post = query.first()

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"the post id ypu provided was not found")

        vote_query = db.query(Vote).filter(Vote.post_id == vote.post_id,Vote.user_id == user.id)
        if vote.vote_dir:
            if vote_query.first():
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"this post has been already liked")
            else:
                new_vote = Vote(post_id=vote.post_id,user_id=user.id)
                db.add(new_vote)
                db.commit()
                db.refresh(new_vote)
                return {"created":new_vote}
        else:
            fetched_vote = vote_query.first() 
            if fetched_vote:
                vote_query.delete(synchronize_session=False)
                db.commit()
                Response(status_code=status.HTTP_204_NO_CONTENT)
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"the post have no votes")                
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"invalid data")
