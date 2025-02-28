from fastapi import  Response, status, HTTPException, Depends, APIRouter
from typing import  List
from .. import models, schemas 
from ..database import  get_db
from sqlalchemy.orm import Session


router = APIRouter()

@router.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db : Session = Depends(get_db)):
    posts = db.query(models.Posty).all()
    return  posts




@router.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Post , db: Session = Depends(get_db)):
    #new_post = models.Posty(title=post.title, content=post.content, published=post.published)
    new_post = models.Posty(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, response: Response , db: Session = Depends(get_db)):
    post = db.query(models.Posty).filter(models.Posty.id == post_id).first()
    if post:
        return post
    
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail="Post not found")




@router.delete("/posts/{post_id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int , db: Session = Depends(get_db)):
    post = db.query(models.Posty).filter(models.Posty.id == post_id).first()
    if post:
        db.delete(post)
        #post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail="Post not found")



@router.put("/posts/{post_id}")
def update_post(post_id: int, post: schemas.Post, db: Session = Depends(get_db)):
    updated_post = db.query(models.Posty).filter(models.Posty.id == post_id)
    if updated_post.first():
        updated_post.update(post.dict() , synchronize_session=False)
        db.commit()
        return  updated_post.first()
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail="Post not found")

