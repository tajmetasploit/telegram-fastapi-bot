"""
import asyncio
from app.bot import dp, bot

async def main():
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())"""

import asyncio
from app.bot import dp, bot, register_handlers

async def main():
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
