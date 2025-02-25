from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World "}


@app.post("/createposts")
async def create_post(payload: dict = Body(...)):
    print(payload)
    return {"message": f"title: {payload['title']}, content: {payload['content']}"}

