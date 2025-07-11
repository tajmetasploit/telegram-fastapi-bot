# tests/test_crud.py

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







# tests/test_bot.py

import pytest
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from unittest.mock import AsyncMock, patch
from app.bot import process_insert, start_insert, fallback_save, Form

class DummyMessage:
    def __init__(self, text):
        self.text = text
        self.answer = AsyncMock()

@pytest.mark.asyncio
async def test_start_insert_sets_state():
    message = DummyMessage("вставить")
    state = AsyncMock()
    
    await start_insert(message, state)
    
    state.set_state.assert_called_once_with(Form.inserting)
    message.answer.assert_called_once_with("✏️ Пожалуйста, введите сообщение для вставки:")

@pytest.mark.asyncio
async def test_process_insert_new_message():
    message = DummyMessage("Новое сообщение")
    state = AsyncMock()
    
    mock_db = AsyncMock()
    
    with patch("app.bot.get_db", return_value=iter([mock_db])), \
         patch("app.crud.search_messages", return_value=[]), \
         patch("app.crud.create_message") as mock_create:
        
        mock_create.return_value.id = 1
        
        await process_insert(message, state)
        message.answer.assert_called_once_with("✅ Сообщение сохранено с ID: 1")
        state.clear.assert_called_once()

@pytest.mark.asyncio
async def test_fallback_duplicate_message():
    message = DummyMessage("Привет")
    state = AsyncMock()
    
    mock_db = AsyncMock()
    
    with patch("app.bot.get_db", return_value=iter([mock_db])), \
         patch("app.crud.search_messages", return_value=[{"id": 1, "text": "Привет"}]):
        
        await fallback_save(message, state)
        message.answer.assert_called_once_with("⚠️ Такое сообщение уже есть в базе данных.")
