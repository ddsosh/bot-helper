import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv
from database import init_db
from handlers.auth import router as auth_router
from handlers.movies import router as movies_router
from keyboards.menu import router as menu_router
from handlers.notes import router as notes_router
from handlers.subs import router as subs_router
from handlers.cabinet import router as cabinet_router
from scheduler import start_scheduler

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
dp = Dispatcher()

async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")
    proxy_url = getenv("BOT_PROXY")
    session = AiohttpSession(proxy=proxy_url, timeout=90) if proxy_url else AiohttpSession(timeout=90)
    bot = Bot(token=TOKEN, session=session)
    await init_db()
    dp.include_router(auth_router)
    dp.include_router(movies_router)
    dp.include_router(menu_router)
    dp.include_router(notes_router)
    dp.include_router(subs_router)
    dp.include_router(cabinet_router)
    print("Bot started")
    start_scheduler(bot)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
