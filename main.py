from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from database import SessionLocal, engine
from models import User
from schemas import UserCreate, User, Post, PostCreate
from typing import List
from sqlalchemy.orm import Session
from services import get_db, get_user_by_email, save_user_to_db, get_users, create_database, get_user, save_post_to_db, get_post, get_posts, del_post, upd_post

app = FastAPI()
create_database()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": "Validation error", "details": exc.errors()},
    )

@app.on_event("startup")
def startup():
    engine.connect()

@app.on_event("shutdown")
def shutdown():
    engine.dispose()


@app.post("/usres/", response_model=User)
def create_user(user: UserCreate, db: Session= Depends(get_db)):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400,detail="woops the email is in use")
    return save_user_to_db(db=db, user=user)  

@app.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_users(db=db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404, detail="Sorry this use is not exist." 
        )
    return db_user

@app.post("/users/{user_id}/posts/", response_model= Post)
def create_post(user_id:int, post : PostCreate , db: Session = Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404, detail="Sorry this use is not exist." 
        )
    return save_post_to_db(db=db, post=post, user_id=user_id)

@app.get("/posts/", response_model=List[Post])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    post = get_posts(db=db, skip=skip, limit=limit)
    return post

@app.get("/posts/{post_id}", response_model=Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = get_post(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(
            status_code=404, detail="Sorry this use is not exist." 
        )
    return db_post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    del_post(db=db,post_id=post_id)
    return{"message", "Successfully deleted with post id {post_id}"}


@app.put("/posts/{post_id}", response_model=Post)
def update_post(post_id: int,post: PostCreate ,db: Session = Depends(get_db)):
    return upd_post(db=db, post=post, post_id=post_id)



# @app.get("/users", response_model=List[User])
# def get_all_users():
#     db = SessionLocal()
#     users = db.query(User).all()
#     return users


# @app.post("/users", status_code=201)
# def create_user(user: UserCreate):
#     db = SessionLocal()
#     db_user = User(username=user.username, email=user.email)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     db = SessionLocal()
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# @app.put("/users/{user_id}")
# def update_user(user_id: int, user: UserUpdate):
#     db = SessionLocal()
#     db_user = db.query(User).filter(User.id == user_id).first()
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     for field, value in user.dict(exclude_unset=True).items():
#         setattr(db_user, field, value)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @app.delete("/users/{user_id}")
# def delete_user(user_id: int):
#     db = SessionLocal()
#     db_user = db.query(User).filter(User.id == user_id).first()
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.delete(db_user)
#     db.commit()
#     return {"message": "User deleted"}


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="localhost", port=8000, reload=True)