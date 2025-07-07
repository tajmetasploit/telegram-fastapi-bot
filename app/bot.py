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

from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "8058688084:AAG0LreV_E0vaQPqEW9QC9-TYRCDgp4lyp4"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# 🧠 FSM states
class Form(StatesGroup):
    inserting = State()
    updating_id = State()
    updating_text = State()
    deleting = State()
    searching = State()
    listing = State()
    #searching_by_id = State()  


# 🧾 Menu keyboard (добавили "List All")
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Start"), KeyboardButton(text="Insert"), KeyboardButton(text="Update")],
        [KeyboardButton(text="Delete"), KeyboardButton(text="Search"), KeyboardButton(text="List All")]
    ],
    resize_keyboard=True
)

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@dp.message(CommandStart())
async def on_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("👋 Welcome! Choose an action below:", reply_markup=menu_keyboard)



# 🆕 Insert
@dp.message(F.text.lower() == "insert")
async def start_insert(message: types.Message, state: FSMContext):
    await state.set_state(Form.inserting)
    await message.answer("✏️ Please type the message to insert:")

# 📥 Insert message directly (skip duplicates)
@dp.message(Form.inserting)
async def process_insert(message: types.Message, state: FSMContext):
    db = next(get_db())
    if crud.search_messages(db, message.text.strip()):
        await message.answer("⚠️ This message already exists in the database.")
    else:
        new_msg = crud.create_message(db, message.text.strip())
        await message.answer(f"✅ Message saved with ID: {new_msg.id}")
    await state.clear()

# 🔄 Update
@dp.message(F.text.lower() == "update")
async def start_update(message: types.Message, state: FSMContext):
    await state.set_state(Form.updating_id)
    await message.answer("✏️ Enter the ID of the message to update:")

@dp.message(Form.updating_id)
async def update_get_id(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Please enter a valid numeric ID.")
        return
    await state.update_data(update_id=int(message.text))
    await state.set_state(Form.updating_text)
    await message.answer("✏️ Now enter the new text:")

@dp.message(Form.updating_text)
async def update_get_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get("update_id")
    db = next(get_db())
    updated = crud.update_message(db, msg_id, message.text.strip())
    if updated:
        await message.answer(f"✅ Message {msg_id} updated.")
    else:
        await message.answer("❌ Message not found.")
    await state.clear()

# 🗑 Delete
@dp.message(F.text.lower() == "delete")
async def start_delete(message: types.Message, state: FSMContext):
    await state.set_state(Form.deleting)
    await message.answer("🗑 Please enter the ID of the message to delete:")

@dp.message(Form.deleting)
async def process_delete(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Enter a valid numeric ID.")
        return
    db = next(get_db())
    deleted = crud.delete_message(db, int(message.text.strip()))
    if deleted:
        await message.answer("✅ Message deleted.")
    else:
        await message.answer("❌ Message not found.")
    await state.clear()



# 🔍 Search
@dp.message(F.text.lower() == "search")
async def start_search(message: types.Message, state: FSMContext):
    await state.set_state(Form.searching)
    await message.answer("🔍 Enter a keyword to search:")

@dp.message(Form.searching)
async def process_search(message: types.Message, state: FSMContext):
    db = next(get_db())
    results = crud.search_messages(db, message.text.strip())
    if not results:
        await message.answer("🔎 No matches found.")
    else:
        response = "\n".join(f"{m.id}: {m.text}" for m in results)
        await message.answer(response)
    await state.clear()



# 📜 List All
@dp.message(F.text.lower() == "list all")
async def list_all_messages(message: types.Message, state: FSMContext):
    db = next(get_db())
    all_msgs = crud.get_all_messages(db)
    if not all_msgs:
        await message.answer("📭 No messages saved yet.")
        return

    MAX_LEN = 4000  # Telegram max text limit is ~4096
    lines = [f"{m.id}: {m.text}" for m in all_msgs]
    current = ""
    for line in lines:
        if len(current) + len(line) + 1 > MAX_LEN:
            await message.answer(current)
            current = ""
        current += line + "\n"
    if current:
        await message.answer(f"📝 All Messages:\n{current}")



"""@dp.message(F.text.lower() == "search by id")
async def start_search_by_id(message: types.Message, state: FSMContext):
    await state.set_state(Form.searching_by_id)
    await message.answer("🔍 Enter the ID to search:")

@dp.message(Form.searching_by_id)
async def process_search_by_id(message: types.Message, state: FSMContext):
    if not message.text.strip().isdigit():
        await message.answer("⚠️ Please enter a valid numeric ID.")
        return

    msg_id = int(message.text.strip())
    db = next(get_db())
    msg = crud.get_message_by_id(db, msg_id)

    if msg:
        await message.answer(f"📝 Found: {msg.id}: {msg.text}")
    else:
        await message.answer("❌ No message found with that ID.")
    await state.clear()
"""


# ❓ Unknown messages (skip known menu & duplicates)
@dp.message()
async def fallback_save(message: types.Message, state: FSMContext):
    text = message.text.strip()
    lower = text.lower()
    known_buttons = {"start", "insert", "update", "delete", "search", "list all"}

    if lower in known_buttons:
        await message.answer("❗ Please select an action from the menu.")
        return

    db = next(get_db())
    if crud.search_messages(db, text):
        await message.answer("⚠️ This message already exists in the database.")
    else:
        new_msg = crud.create_message(db, text)
        await message.answer(f"✅ Message saved with ID: {new_msg.id}")


# 🔄 Start bot
async def start_bot():
    await dp.start_polling(bot)
