from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from database import SessionLocal, engine
from models import User
from schemas import UserCreate, User
from typing import List
from sqlalchemy.orm import Session
from services import get_db, get_user_by_email, create_user, get_users

app = FastAPI()

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
    return create_user(db=db, user=user)  

@app.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_users(db=db, skip=skip, limit=limit)
    return users
    


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