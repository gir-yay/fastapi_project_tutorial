from pydantic import BaseModel, EmailStr
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
        #orm_mode = True
        from_attributes = True



class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id : int
    username : str
    email : EmailStr

    class Config:
        from_attributes  = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


