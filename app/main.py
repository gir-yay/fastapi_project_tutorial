from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine , SessionLocal, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    published: bool=False
    



@app.get("/")
async def root():
    return {"message": "Hello World "}


@app.get("/posts")
def get_posts(db : Session = Depends(get_db)):
    posts = db.query(models.Posty).all()
    return {"data": posts}




@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post , db: Session = Depends(get_db) ):
    #new_post = models.Posty(title=post.title, content=post.content, published=post.published)
    new_post = models.Posty(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}





@app.get("/posts/{post_id}")
def get_post(post_id: int, response: Response , db: Session = Depends(get_db)):
    post = db.query(models.Posty).filter(models.Posty.id == post_id).first()
    if post:
        return {"data": post}
    
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail="Post not found")




@app.delete("/posts/{post_id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int , db: Session = Depends(get_db)):
    post = db.query(models.Posty).filter(models.Posty.id == post_id).first()
    if post:
        db.delete(post)
        #post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail="Post not found")



@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post, db: Session = Depends(get_db)):
    updated_post = db.query(models.Posty).filter(models.Posty.id == post_id)
    if updated_post.first():
        updated_post.update(post.dict() , synchronize_session=False)
        db.commit()
        return {"data": updated_post.first()}
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail="Post not found")