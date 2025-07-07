# telegram_fastapi_bot
# app/main.py

import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.bot import dp, start_bot  # your telegram handlers and bot polling
from app.routers import messages  # your FastAPI router for API endpoints

app = FastAPI(title="Telegram + FastAPI Project")

# Optional: enable CORS if frontend will call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your API routers
app.include_router(messages.router, prefix="/messages", tags=["messages"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Telegram + FastAPI project!"}

# Startup event: run Telegram bot polling in background
@app.on_event("startup")
async def on_startup():
    asyncio.create_task(start_bot())

# Optional shutdown event to cleanup if needed
@app.on_event("shutdown")
async def on_shutdown():
    # Here you can cleanup resources if needed
    pass
# telegram-fastapi-bot
