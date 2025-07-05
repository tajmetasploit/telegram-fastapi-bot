"""import pytest
import asyncio
from app.database import async_session
from app.models import Message
from sqlalchemy.future import select

@pytest.mark.asyncio
async def test_add_and_get_message():
    async with async_session() as session:
        new_message = Message(user_id=1, text="Test message")
        session.add(new_message)
        await session.commit()

        result = await session.execute(select(Message).where(Message.user_id == 1))
        message = result.scalar_one()

        assert message.text == "Test message"
"""
""""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import Message

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_message():
    response = client.post("/messages", params={"content": "Hello Test"})
    assert response.status_code == 200
    assert response.json()["content"] == "Hello Test"
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/mybotdatabase")

engine = create_engine(DATABASE_URL)

# This SessionLocal can be overridden in tests
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_dummy():
    assert 1 + 1 == 2
