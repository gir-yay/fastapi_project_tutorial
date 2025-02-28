from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    published: bool=False


class CreatePost(Post):
    pass
    

