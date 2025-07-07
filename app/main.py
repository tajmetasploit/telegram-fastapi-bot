"""# app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}
"""
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db, Base, engine
from app.models import Message

from fastapi import FastAPI
from app.bot import start_bot  # import the bot startup
import asyncio

app = FastAPI()

# Optional: create tables automatically (for dev)
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}



@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_bot())  # runs the bot in background


@app.post("/messages")
def create_message(content: str, db: Session = Depends(get_db)):
    new_message = Message(text=content)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return {"id": new_message.id, "content": new_message.text}

