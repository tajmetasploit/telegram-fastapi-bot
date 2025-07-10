"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, Base, engine
from app.models import Message
from app.bot import start_bot
import asyncio

app = FastAPI(title="Telegram + FastAPI Project")

# 📦 Create tables in DB
Base.metadata.create_all(bind=engine)

# 🟢 Root
@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}

# 🟢 List all messages
@app.get("/messages")
def get_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).all()
    return [{"id": m.id, "content": m.text} for m in messages]

# 🟢 Get message by ID
@app.get("/messages/{message_id}")
def get_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"id": message.id, "content": message.text}

# ➕ Create message
@app.post("/messages")
def create_message(content: str, db: Session = Depends(get_db)):
    new_message = Message(text=content)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return {"id": new_message.id, "content": new_message.text}

# ✏️ Update message by ID
@app.put("/messages/{message_id}")
def update_message(message_id: int, new_content: str, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    message.text = new_content
    db.commit()
    db.refresh(message)
    return {"id": message.id, "content": message.text}

# ❌ Delete message by ID
@app.delete("/messages/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(message)
    db.commit()
    return {"detail": f"Message with ID {message_id} deleted successfully."}

# 🚀 Run Telegram bot when FastAPI starts
@app.on_event("startup")
async def on_startup():
    asyncio.create_task(start_bot())
"""

"""from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db, Base, engine
from app.models import Message
from app.bot import start_bot
import asyncio

app = FastAPI(title="Проект Telegram + FastAPI")

# 📦 Создание таблиц при запуске
Base.metadata.create_all(bind=engine)

# 🟢 Корневой эндпоинт
@app.get("/")
async def root():
    return {"message": "👋 Привет! FastAPI работает."}

# 🟢 Получить все сообщения
@app.get("/messages", summary="Получить список всех сообщений")
def get_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).all()
    return [{"id": m.id, "текст": m.text} for m in messages]

# 🟢 Получить сообщение по ID
@app.get("/messages/{message_id}", summary="Получить сообщение по ID")
def get_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="❌ Сообщение не найдено.")
    return {"id": message.id, "текст": message.text}

# ➕ Создать сообщение
@app.post("/messages", summary="Создать новое сообщение")
def create_message(content: str = Query(..., description="Текст нового сообщения"), db: Session = Depends(get_db)):
    new_message = Message(text=content)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return {"id": new_message.id, "текст": new_message.text}

# ✏️ Обновить сообщение
@app.put("/messages/{message_id}", summary="Обновить существующее сообщение")
def update_message(
    message_id: int,
    new_content: str = Query(..., description="Новый текст сообщения"),
    db: Session = Depends(get_db)
):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="❌ Сообщение не найдено.")
    message.text = new_content
    db.commit()
    db.refresh(message)
    return {"id": message.id, "текст": message.text}

# ❌ Удалить сообщение
@app.delete("/messages/{message_id}", summary="Удалить сообщение по ID")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="❌ Сообщение не найдено.")
    db.delete(message)
    db.commit()
    return {"detail": f"✅ Сообщение с ID {message_id} успешно удалено."}

# 🚀 Запуск Telegram-бота вместе с FastAPI
@app.on_event("startup")
async def on_startup():
    asyncio.create_task(start_bot())
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db, Base, engine
from app.models import Message
from app.bot import start_bot
import asyncio
import os
app = FastAPI(title="Проект Telegram + FastAPI")

print("DATABASE_URL is:", os.getenv("DATABASE_URL"))


# 📦 Создание таблиц при запуске
Base.metadata.create_all(bind=engine)

# 🟢 Корневой эндпоинт
@app.get("/")
async def root():
    return {"message": "👋 Привет! FastAPI работает."}

# 🟢 Получить все сообщения
@app.get("/messages", summary="Получить список всех сообщений")
def get_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).all()
    return [{"id": m.id, "текст": m.text} for m in messages]

# 🟢 Получить сообщение по ID
@app.get("/messages/{message_id}", summary="Получить сообщение по ID")
def get_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="❌ Сообщение не найдено.")
    return {"id": message.id, "текст": message.text}

# ➕ Создать сообщение
@app.post("/messages", summary="Создать новое сообщение")
def create_message(content: str = Query(..., description="Текст нового сообщения"), db: Session = Depends(get_db)):
    new_message = Message(text=content)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return {"id": new_message.id, "текст": new_message.text}

# ✏️ Обновить сообщение
@app.put("/messages/{message_id}", summary="Обновить существующее сообщение")
def update_message(
    message_id: int,
    new_content: str = Query(..., description="Новый текст сообщения"),
    db: Session = Depends(get_db)
):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="❌ Сообщение не найдено.")
    message.text = new_content
    db.commit()
    db.refresh(message)
    return {"id": message.id, "текст": message.text}

# ❌ Удалить сообщение
@app.delete("/messages/{message_id}", summary="Удалить сообщение по ID")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="❌ Сообщение не найдено.")
    db.delete(message)
    db.commit()
    return {"detail": f"✅ Сообщение с ID {message_id} успешно удалено."}

# 🚀 Запуск Telegram-бота вместе с FastAPI
@app.on_event("startup")
async def on_startup():
    # Запускаем бота в отдельной задаче
    asyncio.create_task(start_bot())


app = FastAPI()

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(start_bot())  # Start Telegram bot as background task

