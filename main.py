from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool=False
    rating : Optional[int] = None



@app.get("/")
async def root():
    return {"message": "Hello World "}


@app.post("/createposts")
async def create_post(post: Post):
    print(post)
    print(post.dict())
    return {"message": f"title: {post.title}, content: {post.content}, published: {post.published}"}
    #async def create_post(payload: dict = Body(...)):
    #print(payload)
    #return {"message": f"title: {payload['title']}, content: {payload['content']}"}

