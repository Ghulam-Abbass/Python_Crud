from pydantic import BaseModel
from typing import List
from datetime import datetime

#The main use of this modules is to describe the relations between our object becuase we are using the orm method.
class PostBase(BaseModel): # i create this postBase class that it would be inculde on every item
    title: str
    content: str

class PostCreate(PostBase): # then here i inherit the PostBase class
    pass  # where i just want to pass all the things

class Post(PostBase): # here as well i inherit my PostBase class becuase i want to show post results with postbase
    id: int
    owner_id: int
    date_created: datetime
    date_last_updated: datetime

    class Config:
        orm_mode = True   

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase): 
    # here i want to create the user using email and password that's why i extend the Userbase as well
    password: str

class User(UserBase):
# this response i will get when i will hit my get endpoint using id and as i extend userbase it will also show email as well to us
    id: int
    is_active: bool    
    posts: List[Post] = []

    class Config:
        orm_mode = True
