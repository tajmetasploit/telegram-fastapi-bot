# tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.models import Message

# 🔧 Настройка тестовой базы
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🧪 Фикстура базы данных
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

# ⛓ Подмена зависимости get_db
@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

# 🌱 Тест: корневой эндпоинт
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "👋 Привет! FastAPI запущен."}

# 🆕 Тест: создание нового сообщения
def test_create_message(client):
    response = client.post("/messages", params={"content": "Hello FastAPI"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data and "text" in data
    assert data["text"] == "Hello FastAPI"

# 📋 Тест: получить все сообщения
def test_get_all_messages(client):
    client.post("/messages", params={"content": "Msg 1"})
    client.post("/messages", params={"content": "Msg 2"})
    response = client.get("/messages")
    assert response.status_code == 200
    messages = response.json()
    assert len(messages) == 2

# 🔍 Тест: получить сообщение по ID
def test_get_message_by_id(client):
    post_resp = client.post("/messages", params={"content": "Find me"})
    msg_id = post_resp.json()["id"]

    get_resp = client.get(f"/messages/{msg_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["text"] == "Find me"

# 📝 Тест: обновление сообщения
def test_update_message(client):
    post_resp = client.post("/messages", params={"content": "Old text"})
    msg_id = post_resp.json()["id"]

    put_resp = client.put(f"/messages/{msg_id}", params={"new_content": "Updated text"})
    assert put_resp.status_code == 200
    assert put_resp.json()["text"] == "Updated text"

# ❌ Тест: обновление несуществующего сообщения
def test_update_not_found(client):
    resp = client.put("/messages/999", params={"new_content": "?"})
    assert resp.status_code == 404

# 🗑️ Тест: удаление сообщения
def test_delete_message(client):
    post_resp = client.post("/messages", params={"content": "To delete"})
    msg_id = post_resp.json()["id"]

    del_resp = client.delete(f"/messages/{msg_id}")
    assert del_resp.status_code == 200
    assert "удалено" in del_resp.json()["detail"]

# ❌ Тест: удаление несуществующего сообщения
def test_delete_not_found(client):
    del_resp = client.delete("/messages/12345")
    assert del_resp.status_code == 404




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
