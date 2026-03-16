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
        return

    # Message event: clear reply keyboard, then send inline menu
    try:
        remove_msg = await event.answer(" ", reply_markup=ReplyKeyboardRemove())
        try:
            await remove_msg.delete()
        except Exception:
            pass
    except Exception:
        pass

    await event.answer(text, reply_markup=keyboard)
