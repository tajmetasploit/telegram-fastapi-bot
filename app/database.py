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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session
from fastapi import Depends
from dotenv import load_dotenv
import os

# Load environment variables from .env file (for local development)
load_dotenv()

# Get individual DB connection params (used on Railway)
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD") or os.getenv("POSTGRES_PASSWORD")
PGHOST = os.getenv("PGHOST") or os.getenv("RAILWAY_PRIVATE_DOMAIN")
PGPORT = os.getenv("PGPORT", "5432")
PGDATABASE = os.getenv("PGDATABASE")

# Build DATABASE_URL manually if all parts exist
if PGUSER and PGPASSWORD and PGHOST and PGDATABASE:
    DATABASE_URL = f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"
else:
    # Fallback to DATABASE_URL directly (from .env) or local
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/mybotdatabase")

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for injecting DB session into routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
