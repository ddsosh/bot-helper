from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from forms.app_states import AppState
from keyboards.menu import (
    get_main_reply_menu,
    get_main_reply_movies,
    get_main_reply_notes,
    get_main_reply_subs,
    get_main_reply_cabinet,
)

router = Router()


@router.message(StateFilter(None), F.text.lower() == "movies")
async def restore_movies_menu(message: Message, state: FSMContext):
    await state.set_state(AppState.movies_menu)
    await message.answer("Movies section", reply_markup=get_main_reply_movies())


@router.message(StateFilter(None), F.text.lower() == "notes")
async def restore_notes_menu(message: Message, state: FSMContext):
    await state.set_state(AppState.notes_menu)
    await message.answer("Notes section", reply_markup=get_main_reply_notes())


@router.message(StateFilter(None), F.text.lower() == "subs")
async def restore_subs_menu(message: Message, state: FSMContext):
    await state.set_state(AppState.subs_menu)
    await message.answer("Subs Menu", reply_markup=get_main_reply_subs())


@router.message(StateFilter(None), F.text.lower() == "cabinet")
async def restore_cabinet_menu(message: Message, state: FSMContext):
    await state.set_state(AppState.cabinet_menu)
    await message.answer("Cabinet", reply_markup=get_main_reply_cabinet())


@router.message(StateFilter(None), F.text.lower() == "back")
async def restore_main_menu(message: Message, state: FSMContext):
    await state.set_state(AppState.main)
    await message.answer("Main menu", reply_markup=get_main_reply_menu())
