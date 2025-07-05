"""import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from aiogram import Router

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8058688084:AAG0LreV_E0vaQPqEW9QC9-TYRCDgp4lyp4")

bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())

router = Router()

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    await message.answer("Hello! I am your Telegram bot powered by FastAPI and aiogram.")

@router.message()
async def echo_message(message: Message):
    await message.answer(f"You said: {message.text}")

dp.include_router(router)
"""

# app/bot.py
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud

import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "8058688084:AAG0LreV_E0vaQPqEW9QC9-TYRCDgp4lyp4"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Welcome to the bot!\n\n"
        "You can use the following commands:\n"
        "🔹 /save <text> - Save a message\n"
        "🔹 /list - Show all saved messages\n"
        "\nJust type /save Hello to try it!"
    )

@dp.message(Command("save"))
async def cmd_save(message: types.Message):
    # Remove the command "/save" and leading/trailing spaces
    text = message.text[len("/save"):].strip()
    if not text:
        await message.answer("❌ Please provide a message after /save.")
        return

    db = SessionLocal()
    try:
        new_msg = crud.create_message(db, text)
        await message.answer(f"✅ Message saved with id: {new_msg.id}")
    finally:
        db.close()


@dp.message(Command("list"))
async def cmd_list(message: types.Message):
    db = next(get_db())
    messages = crud.get_messages(db)
    if not messages:
        await message.answer("No messages saved yet.")
        return
    response = "\n".join(f"{m.id}: {m.text}" for m in messages)
    await message.answer(response)


# Run this from FastAPI startup
async def start_bot():
    await dp.start_polling(bot)



"""from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "8058688084:AAG0LreV_E0vaQPqEW9QC9-TYRCDgp4lyp4"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Helper function to get a DB session
def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("👋 Welcome! Use /save <text> to save a message, or /list to see all messages.")

@dp.message(Command("save"))
async def cmd_save(message: types.Message):
    text = message.text[len("/save"):].strip()
    if not text:
        await message.answer("❌ Please provide a message after /save.")
        return

    db = SessionLocal()
    try:
        new_msg = crud.create_message(db, text)
        await message.answer(f"✅ Message saved with id: {new_msg.id}")
    except Exception as e:
        logging.error(f"Error saving message: {e}")
        await message.answer("❌ Failed to save the message.")
    finally:
        db.close()

@dp.message(Command("list"))
async def cmd_list(message: types.Message):
    db = SessionLocal()
    try:
        messages = crud.get_messages(db)
        if not messages:
            await message.answer("📭 No messages saved yet.")
        else:
            response = "\n".join(f"{m.id}: {m.text}" for m in messages)
            await message.answer(response)
    except Exception as e:
        logging.error(f"Error listing messages: {e}")
        await message.answer("❌ Failed to load messages.")
    finally:
        db.close()

# Function to be called on FastAPI startup
async def start_bot():
    await dp.start_polling(bot)"""
