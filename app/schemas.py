from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Annotated, Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id : int
    username : str
    email : EmailStr

    class Config:
        orm_mode  = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

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
    owner : UserResponse
    #created_at : datetime

    class Config:
        orm_mode = True
        #from_attributes = True




class Token(BaseModel):
    access_token: str 
    token_type: str



class TokenData(BaseModel):
    id: Optional[int] = None
    

class Vote(BaseModel):
    post_id: int
    #dir: conint(le=1)
    dir: Annotated[int, Field(le=1)]



class PostVote(BaseModel):
    post : PostResponse
    votes : int

    class Config:
        orm_mode = True

