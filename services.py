from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate



def create_database():
    return Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first() 

def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "thisisnotsecure"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int, limit: int):
    return db.query(User).offset(skip).limit(limit).all()