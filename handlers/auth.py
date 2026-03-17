from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import ensure_user

router = Router()

#START-------------------------------------------------------------------------------------
@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    from handlers.session import show_main_menu

    await ensure_user(message.from_user.id)
    await show_main_menu(message, state)

#GET_USER-----------------------------------------------------------------------------------

async def get_current_user(event):
    return await ensure_user(event.from_user.id)


def get_user_lang(user):
    if not user or len(user) < 3:
        return "ru"
    return user[2] or "ru"
