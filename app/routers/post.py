from fastapi import  Response, status, HTTPException, Depends, APIRouter
from typing import  List, Optional
from .. import models, schemas , oauth2
from ..database import  get_db
from sqlalchemy.orm import Session


router = APIRouter()

@router.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db : Session = Depends(get_db), limit: int = 3, skip : int = 0, search: Optional[str] = ""):
    posts = db.query(models.Posty).filter(models.Posty.title.contains(search)).limit(limit).offset(skip).all()
    #posts = db.query(models.Posty).filter(models.Posty.user_id == current_user.id).all()
    return  posts




@router.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Post , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #new_post = models.Posty(title=post.title, content=post.content, published=post.published)
    new_post = models.Posty(user_id= current_user.id , **post.dict())
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
def delete_post(post_id: int , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Posty).filter(models.Posty.id == post_id).first()
    
    if post:
        if post.user_id != current_user.id:
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN , detail="You are not allowed to delete this post")
        db.delete(post)
        #post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail="Post not found")



@router.put("/posts/{post_id}")
def update_post(post_id: int, post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    updated_post = db.query(models.Posty).filter(models.Posty.id == post_id)
    updated_post_ = updated_post.first()
    
    if updated_post_:
        if updated_post_.user_id != current_user.id:
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN , detail="You are not allowed to update this post")
        
        updated_post.update(post.dict() , synchronize_session=False)
        db.commit()
        return  updated_post.first()
    
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail="Post not found")

