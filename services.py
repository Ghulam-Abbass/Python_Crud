from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session
from models import User, Post
from schemas import UserCreate, PostCreate
from datetime import datetime



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

def save_user_to_db(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "thisisnotsecure"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int, limit: int):
    return db.query(User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id:int):
    return db.query(User).filter(User.id == user_id).first()

def save_post_to_db(db: Session, post: PostCreate, user_id:int):
    post = Post(**post.dict(), owner_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_posts(db: Session, skip:int, limit:int):
    return db.query(Post).offset(skip).limit(limit).all()

def get_post(db: Session, post_id:int):
    return db.query(Post).filter(Post.id == post_id).first()

def del_post(db: Session, post_id:int):
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()

def upd_post(db: Session, post: PostCreate, post_id:int):
    db_post = get_post(db=db, post_id=post_id)
    db_post.title = post.title
    db_post.content = post.content
    db_post.date_last_update = datetime.now()
    db.commit()
    db.refresh(db_post)
    return db_post