"""from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.orm import sessionmaker
#from dotenv import load_dotenv
import os

#DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/mybotdatabase")

DATABASE_URL = os.getenv("DATABASE_URL") 
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import Depends
from dotenv import load_dotenv

# Only load .env if not in Railway environment
if os.getenv("RAILWAY_ENVIRONMENT") is None:
    load_dotenv()


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")


# Get the DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Raise clear error if missing
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare base class for models
Base = declarative_base()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
