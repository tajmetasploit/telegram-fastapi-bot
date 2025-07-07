"""import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.database import SessionLocal
from app import crud

# ✅ Load token from env or fallback
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "8058688084:AAG0LreV_E0vaQPqEW9QC9-TYRCDgp4lyp4"

# ✅ Create bot and dispatcher instances
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# 🧠 FSM States
class Form(StatesGroup):
    inserting = State()
    updating_id = State()
    updating_text = State()
    deleting = State()
    searching = State()
    listing = State()
    searching_by_id = State()

# 🧾 Keyboard
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Start"), KeyboardButton(text="Insert")],
        [KeyboardButton(text="Update"), KeyboardButton(text="Delete")],
        [KeyboardButton(text="Upgrade"), KeyboardButton(text="Search")],
        [KeyboardButton(text="Search by ID"), KeyboardButton(text="List All")]
    ],
    resize_keyboard=True
)

# 🗃 DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🚀 Handlers
@dp.message(CommandStart())
async def on_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("👋 Welcome! Choose an action below:", reply_markup=menu_keyboard)

# ❗ NOTE: You should paste or import all the remaining handlers here (Insert, Update, Delete, etc.)

# 🔄 Bot launcher (called by FastAPI)
async def start_bot():
    await dp.start_polling(bot)
"""