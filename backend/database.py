from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# MySQL Connection Details
# Replace with your actual MySQL credentials or use environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:@localhost:3308/text_extractor")

# Using SQLite for local development to ensure the app runs immediately without MySQL setup
# SQLALCHEMY_DATABASE_URL = "sqlite:///./text_extractor.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
