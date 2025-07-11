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
