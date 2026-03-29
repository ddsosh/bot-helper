from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from database import delete_note, get_notes, add_note
from forms.app_states import AppState
from handlers.auth import get_current_user, get_user_lang
from keyboards.menu import get_notes_inline_menu, get_label
from handlers.session import show_main_menu


router = Router()


@router.callback_query(F.data == "menu:notes")
async def notes_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.notes_menu)
    user = await get_current_user(callback)
    lang = get_user_lang(user)
    await callback.message.edit_text(get_label(lang, "notes_section"), reply_markup=get_notes_inline_menu(lang))
    await callback.answer()


@router.callback_query(AppState.notes_menu, F.data == "notes:add")
async def add_note_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.add_note_title)
    user = await get_current_user(callback)
    await callback.message.edit_text(get_label(get_user_lang(user), "enter_title"))
    await callback.answer()


@router.message(AppState.add_note_title)
async def note_title(message: Message, state: FSMContext):
    user = await get_current_user(message)
    lang = get_user_lang(user)
    title = (message.text or "").strip()

    if not title:
        await message.answer(get_label(lang, "title_empty"))
        return
    if len(title) > 50:
        await message.answer(get_label(lang, "title_too_long"))
        return

    await state.update_data(title=title)
    await state.set_state(AppState.add_note_date)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=get_label(lang, "skip"), callback_data="skip_note_date")]]
    )
    await message.answer(get_label(lang, "enter_date_or_skip"), reply_markup=keyboard)


@router.message(AppState.add_note_date)
async def note_date(message: Message, state: FSMContext):
    user = await get_current_user(message)
    lang = get_user_lang(user)
    data = await state.get_data()
    title = data.get("title")

    if not title:
        await state.set_state(AppState.add_note_title)
        await message.answer(get_label(lang, "enter_title_first"))
        return

    raw_date = (message.text or "").strip()
    due_date = None if raw_date.lower() == "skip" else raw_date
    if due_date is not None and len(due_date) > 64:
        await message.answer(get_label(lang, "date_value_too_long"))
        return

    if not user:
        await state.set_state(AppState.main)
        await message.answer(get_label("ru", "user_not_found_error"))
        return

    await add_note(user[0], title, due_date)
    await message.answer(get_label(lang, "ok"))

    await state.clear()
    await state.set_state(AppState.notes_menu)
    await message.answer(get_label(lang, "notes_section"), reply_markup=get_notes_inline_menu(lang))


@router.callback_query(AppState.notes_menu, F.data == "notes:list")
async def list_note_handler(callback: CallbackQuery, state: FSMContext):
    user = await get_current_user(callback)
    if not user:
        await callback.answer(get_label("ru", "user_not_found_error"))
        return
    await render_notes_list(callback, state, user[0])
    await callback.answer()


@router.callback_query(AppState.notes_menu, F.data == "delete_note")
async def delete_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.delete_note_number)
    user = await get_current_user(callback)
    lang = get_user_lang(user)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_label(lang, "cancel_delete"), callback_data="cancel_delete_note")]
        ]
    )
    await callback.message.edit_text(get_label(lang, "enter_number_to_delete"), reply_markup=keyboard)
    await callback.answer()


@router.message(AppState.delete_note_number)
async def delete_by_number(message: Message, state: FSMContext):
    user = await get_current_user(message)
    lang = get_user_lang(user)
    data = await state.get_data()
    note_map = data.get("note_map")

    if not note_map:
        await message.answer(get_label(lang, "first_use_list_notes"))
        await state.set_state(AppState.notes_menu)
        return

    try:
        number = int(message.text)
    except (TypeError, ValueError):
        await message.answer(get_label(lang, "enter_valid_number"))
        return

    if number not in note_map:
        await message.answer(get_label(lang, "no_note_with_number"))
        return

    if not user:
        await state.set_state(AppState.main)
        await message.answer(get_label("ru", "user_not_found_error"))
        return

    note_id = note_map[number]
    await delete_note(user[0], note_id)
    await state.set_state(AppState.notes_menu)
    await render_notes_list(message, state, user[0])


@router.callback_query(F.data.startswith("del_note_"))
async def delete_callback(callback: CallbackQuery, state: FSMContext):
    note_id = int(callback.data.split("_")[2])
    user = await get_current_user(callback)
    if not user:
        await callback.answer(get_label("ru", "user_not_found_error"))
        return

    await delete_note(user[0], note_id)
    await render_notes_list(callback, state, user_id=user[0])
    await callback.answer()


@router.callback_query(AppState.delete_note_number, F.data == "cancel_delete_note")
async def cancel_delete_note(callback: CallbackQuery, state: FSMContext):
    user = await get_current_user(callback)
    if not user:
        await callback.answer(get_label("ru", "user_not_found_error"))
        return

    await state.set_state(AppState.notes_menu)
    await render_notes_list(callback, state, user[0])
    await callback.answer()


async def render_notes_list(event, state, user_id: int):
    user = await get_current_user(event)
    lang = get_user_lang(user)
    notes = await get_notes(user_id)
    if not notes:
        if state:
            await state.update_data(note_map={})
            await state.set_state(AppState.notes_menu)

        if isinstance(event, CallbackQuery):
            await event.message.edit_text(get_label(lang, "notes_section"), reply_markup=get_notes_inline_menu(lang))
        else:
            await event.answer(get_label(lang, "notes_section"), reply_markup=get_notes_inline_menu(lang))
        return

    text = get_label(lang, "notes_list_title")
    note_map = {}

    for index, note in enumerate(notes, start=1):
        note_id = note[0]
        title = note[2]
        due_date = note[3]
        date_text = due_date if due_date else get_label(lang, "no_date")
        text += f"{index}. {title}\n{date_text}\n\n"
        note_map[index] = note_id

    if state:
        await state.update_data(note_map=note_map)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_label(lang, "delete"), callback_data="delete_note")],
            [InlineKeyboardButton(text=get_label(lang, "back"), callback_data="menu:notes")],
        ]
    )

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=keyboard)
    else:
        await event.answer(text, reply_markup=keyboard)


@router.callback_query(AppState.add_note_date, F.data == "skip_note_date")
async def skip_note_date(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    title = data.get("title")
    user = await get_current_user(callback)
    lang = get_user_lang(user)

    if not title:
        await state.set_state(AppState.add_note_title)
        await callback.message.answer(get_label(lang, "enter_title_first"))
        await callback.answer()
        return

    if not user:
        await state.set_state(AppState.main)
        await callback.message.answer(get_label("ru", "user_not_found_error"))
        await callback.answer()
        return

    await add_note(user[0], title, None)
    await callback.answer()

    await state.clear()
    await state.set_state(AppState.notes_menu)
    await callback.message.edit_text(get_label(lang, "notes_section"), reply_markup=get_notes_inline_menu(lang))


@router.callback_query(AppState.notes_menu, F.data == "menu:main")
async def back_handler(callback: CallbackQuery, state: FSMContext):
    await show_main_menu(callback, state)
    await callback.answer()
