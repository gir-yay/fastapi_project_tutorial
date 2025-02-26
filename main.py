from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str



@app.get("/")
async def root():
    return {"message": "Hello World "}


@app.post("/createposts")
async def create_post(post: Post):
    print(post)
    return {"message": f"title: {post.title}, content: {post.content}"}
    #async def create_post(payload: dict = Body(...)):
    #print(payload)
    #return {"message": f"title: {payload['title']}, content: {payload['content']}"}

