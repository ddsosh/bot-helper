from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import ensure_user
from forms.app_states import AppState
from keyboards.menu import get_main_reply_menu

router = Router()

#START-------------------------------------------------------------------------------------
@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await ensure_user(message.from_user.id)
    await state.set_state(AppState.main)
    await message.answer("Choose section", reply_markup=get_main_reply_menu())

#GET_USER-----------------------------------------------------------------------------------

async def get_current_user(event):
    return await ensure_user(event.from_user.id)

