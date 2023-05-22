from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uvicorn

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Import your models and schemas here
# from models import User
# from schemas import UserCreate

# Your other route definitions and application code

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

if __name__ == "__main__":
    # Run the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=8000)
