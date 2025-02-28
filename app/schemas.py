from pydantic import BaseModel
from datetime import datetime


# Better be names PostBase
class Post(BaseModel):
    title: str
    content: str
    published: bool=False


class CreatePost(Post):
    pass
    

class PostResponse(BaseModel):
    id : int
    title : str
    content : str
    published : bool
    #created_at : datetime

    class Config:
        orm_mode = True