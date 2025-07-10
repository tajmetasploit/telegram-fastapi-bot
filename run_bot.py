# run_bot.py
import asyncio
from app.bot import dp, bot, register_handlers

async def main():
    print("🤖 Starting Telegram bot...")
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
