from fastapi import  Response, status, HTTPException, Depends, APIRouter
from typing import  List
from .. import models, schemas , utils, oauth2
from ..database import  get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes",
    tags=["Votes"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Posty).filter(models.Posty.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} not found")

    new_vote = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = new_vote.first()

    # if the user wanna like the post
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} already voted on post {vote.post_id}")

        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Post liked"}
    
    # if the user wanna dislike the post
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not liked")
        
        new_vote.delete(synchronize_session=False)
        db.commit()
        return {"message": "Post disliked"}
