from pydantic import BaseModel
from typing import List
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass 

class Post(PostBase):
    id: int
    owner_id: int
    date_created: datetime
    date_last_updated: datetime

    class Config:
        orm_mode = True   

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool    
    posts: List[Post] = []

    class Config:
        orm_mode = True
