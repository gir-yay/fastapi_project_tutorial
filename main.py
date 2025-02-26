from fastapi import FastAPI, Response, status, HTTPException
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



@app.post("/posts", status_code=status.HTTP_201_CREATED)
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



def find_post(post_id: int):
    for post in my_posts:
        if post["id"] == post_id:
            return post
    return None


@app.get("/posts/latest")
def get_latest_post():
    if my_posts:
        return {"data": my_posts[-1]}
    return {"error": "No posts available"}

@app.get("/posts/{post_id}")
def get_post(post_id: int, response: Response):
    post = find_post(post_id)
    if post:
        return {"data": post}

    #response.status_code = 404
    #response.status_code = status.HTTP_404_NOT_FOUND
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail="Post not found")

    #return {"error": "Post not found"}