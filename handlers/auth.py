from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import add_user, get_user_by_telegram_id, verify_user_password
from forms.app_states import AppState
from keyboards.menu import get_main_reply_menu

router = Router()

#START-------------------------------------------------------------------------------------
@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    user = await get_current_user(message)
    if user:
        await message.answer("Enter your password")
        await state.set_state(AppState.verify_password)
        return
    await message.answer("Create an account\nEnter login: ")
    await state.set_state(AppState.login)

#REGISTER----------------------------------------------------------------------------------
@router.message(AppState.login)
async def process_login(message: Message, state: FSMContext):
    login = (message.text or "").strip()
    if len(login) < 3 or len(login) > 32:
        await message.answer("Login must be 3-32 chars")
        return
    await state.update_data(login=login)
    await message.answer("Enter your password")
    await state.set_state(AppState.pas)

@router.message(AppState.pas)
async def process_password(message: Message, state: FSMContext):
    data = await state.get_data()
    login = data.get("login")
    password = (message.text or "").strip()

    if not login:
        await state.set_state(AppState.login)
        await message.answer("Enter login first")
        return
    if len(password) < 6 or len(password) > 64:
        await message.answer("Password must be 6-64 chars")
        return

    created = await add_user(
        telegram_id=message.from_user.id,
        login=login,
        password=password,
    )
    if not created:
        await state.set_state(AppState.main)
        await message.answer(
            "You are already registered\nChoose section",
            reply_markup=get_main_reply_menu(),
        )
        return

    await state.set_state(AppState.main)
    await message.answer("Successful\nYou have been logged in\nChoose section",
                         reply_markup=get_main_reply_menu())

#LOGIN-------------------------------------------------------------------------------------

@router.message(AppState.verify_password)
async def verify_password_handler(message: Message, state: FSMContext):
    password = (message.text or "").strip()

    if len(password) < 6 or len(password) > 64:
        await message.answer("Password must be 6-64 chars")
        return

    ok = await verify_user_password(message.from_user.id, password)
    if not ok:
        await message.answer("Wrong password. Try again")
        return

    await state.set_state(AppState.main)
    await message.answer("Successful\nYou have been logged in\nChoose section",
                         reply_markup=get_main_reply_menu())

#GET_USER-----------------------------------------------------------------------------------

async def get_current_user(event):
    return await get_user_by_telegram_id(event.from_user.id)


