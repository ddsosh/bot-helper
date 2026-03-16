from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from forms.app_states import AppState
from keyboards.menu import get_main_inline_menu

router = Router()


@router.callback_query(F.data == "menu:main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.main)
    await show_main_menu(callback, state)
    await callback.answer()


async def show_main_menu(event, state: FSMContext):
    await state.set_state(AppState.main)
    text = "Choose section"
    keyboard = get_main_inline_menu()

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=keyboard)
    else:
        msg = await event.answer(text, reply_markup=ReplyKeyboardRemove())
        await msg.edit_text(text, reply_markup=keyboard)
