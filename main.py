from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool=False
    rating : Optional[int] = None


my_posts = [
    {"title": "Post 1", "content": "Content 1", "id": 1},
    {"title": "Post 2", "content": "Content 2", "id": 2},
    {"title": "Post 3", "content": "Content 3", "id": 3},
]


@app.get("/")
async def root():
    return {"message": "Hello World "}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}



@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000000)
    my_posts.append(post_dict)
    return {"data": post}



@app.post("/createposts")
async def create_post(post: Post):
    print(post)
    print(post.dict())
    return {"message": f"title: {post.title}, content: {post.content}, published: {post.published}"}
    #async def create_post(payload: dict = Body(...)):
    #print(payload)
    #return {"message": f"title: {payload['title']}, content: {payload['content']}"}

