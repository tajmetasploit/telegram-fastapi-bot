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

"""from fastapi import FastAPI, Depends, HTTPException, Query
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


import asyncio
from fastapi import FastAPI
from app.bot import dp, bot, register_handlers  # Import your bot setup

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    print("🚀 Starting both FastAPI and Telegram Bot")
    register_handlers(dp)

    # Start Telegram bot in background
    asyncio.create_task(dp.start_polling(bot))"""


""""# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db, Base, engine
from app.models import Message
import asyncio
import os
from fastapi import FastAPI, Depends



from fastapi import FastAPI
from app.bot import start_bot  # import the bot startup
import asyncio

app = FastAPI(title="Telegram + FastAPI Project")

# Create tables on startup
Base.metadata.create_all(bind=engine)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "👋 Hello! FastAPI is running."}

# Get all messages
@app.get("/messages", summary="Get all messages")
def get_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).all()
    return [{"id": m.id, "text": m.text} for m in messages]

# Get a message by ID
@app.get("/messages/{message_id}", summary="Get message by ID")
def get_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="❌ Message not found.")
    return {"id": message.id, "text": message.text}

# Create a message
@app.post("/messages", summary="Create new message")
def create_message(content: str = Query(...), db: Session = Depends(get_db)):
    new_message = Message(text=content)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return {"id": new_message.id, "text": new_message.text}

# Update a message
@app.put("/messages/{message_id}", summary="Update a message")
def update_message(message_id: int, new_content: str = Query(...), db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="❌ Message not found.")
    message.text = new_content
    db.commit()
    db.refresh(message)
    return {"id": message.id, "text": message.text}

# Delete a message
@app.delete("/messages/{message_id}", summary="Delete a message")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="❌ Message not found.")
    db.delete(message)
    db.commit()
    return {"detail": f"✅ Message with ID {message_id} deleted."}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_bot())  # runs the bot in background

# Optional: start Telegram bot in background (not recommended with polling)
# Instead, use a separate `run_bot.py` for polling"""

"""
# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db, Base, engine
from app.models import Message
import asyncio
import os
from fastapi import FastAPI, Depends

from fastapi import FastAPI
from app.bot import start_bot  # import the bot startup
import asyncio

app = FastAPI(title="Telegram + FastAPI Project")

# Create tables on startup
Base.metadata.create_all(bind=engine)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "👋 Hello! FastAPI is running."}

# Get all messages
@app.get("/messages", summary="Get all messages")
def get_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).all()
    return [{"id": m.id, "text": m.text} for m in messages]

# Get a message by ID
@app.get("/messages/{message_id}", summary="Get message by ID")
def get_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="❌ Message not found.")
    return {"id": message.id, "text": message.text}

# Create a message
@app.post("/messages", summary="Create new message")
def create_message(content: str = Query(...), db: Session = Depends(get_db)):
    new_message = Message(text=content)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return {"id": new_message.id, "text": new_message.text}

# Update a message
@app.put("/messages/{message_id}", summary="Update a message")
def update_message(message_id: int, new_content: str = Query(...), db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="❌ Message not found.")
    message.text = new_content
    db.commit()
    db.refresh(message)
    return {"id": message.id, "text": message.text}

# Delete a message
@app.delete("/messages/{message_id}", summary="Delete a message")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="❌ Message not found.")
    db.delete(message)
    db.commit()
    return {"detail": f"✅ Message with ID {message_id} deleted."}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_bot())  # runs the bot in background

if __name__ == "__main__":
    import os
    import uvicorn
    import asyncio
    from app.bot import start_bot

    async def run():
        asyncio.create_task(start_bot())  # Start the bot
        port = int(os.environ.get("PORT", 3000))
        config = uvicorn.Config("app.main:app", host="0.0.0.0", port=port)
        server = uvicorn.Server(config)
        await server.serve()

    asyncio.run(run())


# Optional: start Telegram bot in background (not recommended with polling)
# Instead, use a separate `run_bot.py` for polling


# ✅ Railway-compatible run block (added below)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)

"""
# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db, Base, engine
from app.models import Message
import asyncio
import os
from fastapi import FastAPI, Depends

from fastapi import FastAPI
from app.bot import start_bot  # импорт запуска бота
import asyncio

app = FastAPI(title="Проект Telegram + FastAPI")

# Создание таблиц при старте приложения
Base.metadata.create_all(bind=engine)

# Корневой эндпоинт
@app.get("/")
async def root():
    return {"message": "👋 Привет! FastAPI запущен."}



# Получить сообщение по ID
@app.get("/messages/{message_id}", summary="Получить сообщение по ID")
def get_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="❌ Сообщение не найдено.")
    return {"id": message.id, "text": message.text}

# Создать новое сообщение
@app.post("/messages", summary="Создать новое сообщение")
def create_message(content: str = Query(...), db: Session = Depends(get_db)):
    new_message = Message(text=content)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return {"id": new_message.id, "text": new_message.text}

# Обновить сообщение
@app.put("/messages/{message_id}", summary="Обновить сообщение")
def update_message(message_id: int, new_content: str = Query(...), db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="❌ Сообщение не найдено.")
    message.text = new_content
    db.commit()
    db.refresh(message)
    return {"id": message.id, "text": message.text}

# Удалить сообщение
@app.delete("/messages/{message_id}", summary="Удалить сообщение")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="❌ Сообщение не найдено.")
    db.delete(message)
    db.commit()
    return {"detail": f"✅ Сообщение с ID {message_id} удалено."}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_bot())  # запуск бота в фоне

if __name__ == "__main__":
    import os
    import uvicorn
    import asyncio
    from app.bot import start_bot

    async def run():
        asyncio.create_task(start_bot())  # запуск бота
        port = int(os.environ.get("PORT", 3000))
        config = uvicorn.Config("app.main:app", host="0.0.0.0", port=port)
        server = uvicorn.Server(config)
        await server.serve()

    asyncio.run(run())


# Опционально: запуск Telegram бота в фоне (не рекомендуется с polling)
# Лучше использовать отдельный `run_bot.py` для polling


# ✅ Блок запуска, совместимый с Railway (добавлен ниже)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
