"""# tests/test_crud.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models, crud
from app.database import Base  # Base = declarative_base()

# ⚙️ Тестовая SQLite база в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔧 Фикстура для базы данных
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)  # Создаем таблицы
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)  # Очищаем после теста

# 🧪 Тест: create_message
def test_create_message(db):
    msg = crud.create_message(db, "Hello!")
    assert msg.id is not None
    assert msg.text == "Hello!"

# 🧪 Тест: update_message
def test_update_message(db):
    msg = crud.create_message(db, "Old text")
    updated = crud.update_message(db, msg.id, "New text")
    assert updated.text == "New text"

# 🧪 Тест: delete_message
def test_delete_message(db):
    msg = crud.create_message(db, "To be deleted")
    result = crud.delete_message(db, msg.id)
    assert result is True
    assert crud.delete_message(db, msg.id) is False  # Повторное удаление — False

# 🧪 Тест: search_messages
def test_search_messages(db):
    crud.create_message(db, "Apple")
    crud.create_message(db, "Banana")
    crud.create_message(db, "apple pie")

    results = crud.search_messages(db, "apple")
    assert len(results) == 2
    assert all("apple" in msg.text.lower() for msg in results)

# 🧪 Тест: get_messages
def test_get_messages(db):
    crud.create_message(db, "First")
    crud.create_message(db, "Second")
    all_msgs = crud.get_messages(db)
    assert len(all_msgs) == 2
"""