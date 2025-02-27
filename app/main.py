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
    

while True:
    try:
        conn = psycopg2.connect(
            dbname="fastapi_db",
            user="user",
            password="secret",
            host="localhost",
            port="5432",
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()
        break

    except Exception as e:
        print(e)
        time.sleep(5)



@app.get("/")
async def root():
    return {"message": "Hello World "}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()   
    return {"data": new_post}




@app.get("/posts/{post_id}")
def get_post(post_id: int, response: Response):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    if post:
        return {"data": post}
    
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail="Post not found")




@app.delete("/posts/{post_id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s returning *", (post_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail="Post not found")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    #raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail="Post not found")



@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, post_id))
    updated_post = cursor.fetchone()
    if updated_post:
        conn.commit()
        return {"data": updated_post}
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail="Post not found")