import asyncio
from app.bot import dp, bot

async def main():
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

"""
# run_bot.py
import asyncio
import uvicorn
from uvicorn.config import Config
from uvicorn.server import Server
from app.main import app
from app.bot import start_bot

async def start_all():
    config = Config(app=app, host="0.0.0.0", port=8000, loop="asyncio")
    server = Server(config)

    bot_task = asyncio.create_task(start_bot())
    api_task = asyncio.create_task(server.serve())

    await asyncio.gather(bot_task, api_task)

if __name__ == "__main__":
    asyncio.run(start_all())

"""