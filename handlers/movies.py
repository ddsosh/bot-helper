from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from keyboards.menu import get_movies_inline_menu, get_label
from handlers.auth import get_current_user, get_user_lang
from database import get_movies, delete_movie, add_movie
from forms.app_states import AppState
from handlers.session import show_main_menu


router = Router()


@router.callback_query(F.data == "menu:movies")
async def movies_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.movies_menu)
    user = await get_current_user(callback)
    lang = get_user_lang(user)
    await callback.message.edit_text(get_label(lang, "movies_section"), reply_markup=get_movies_inline_menu(lang))
    await callback.answer()


@router.callback_query(AppState.movies_menu, F.data == "movies:add")
async def add_movie_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.add_movie_title)
    user = await get_current_user(callback)
    await callback.message.edit_text(get_label(get_user_lang(user), "enter_title"))
    await callback.answer()


@router.message(AppState.add_movie_title)
async def movie_title(message: Message, state: FSMContext):
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
    await state.set_state(AppState.add_movie_type)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=get_label(lang, "movie_type_movie"), callback_data="movie_type:M"),
                InlineKeyboardButton(text=get_label(lang, "movie_type_series"), callback_data="movie_type:S"),
            ]
        ]
    )
    await message.answer(get_label(lang, "choose_movie_type"), reply_markup=keyboard)


@router.callback_query(AppState.add_movie_type, F.data.startswith("movie_type:"))
async def movie_type(callback: CallbackQuery, state: FSMContext):
    user = await get_current_user(callback)
    lang = get_user_lang(user)
    type_ = callback.data.split(":", 1)[1]
    if type_ not in {"M", "S"}:
        await callback.answer()
        return

    await state.update_data(type_=type_)
    await state.set_state(AppState.add_movie_comment)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_label(lang, "skip"), callback_data="skip_movie_comment")]
        ]
    )
    await callback.message.edit_text(get_label(lang, "enter_comment_or_skip"), reply_markup=keyboard)
    await callback.answer()


@router.message(AppState.add_movie_comment)
async def movie_comment(message: Message, state: FSMContext):
    data = await state.get_data()
    title = data["title"]
    type_ = data["type_"]
    comment = (message.text or "").strip()

    user = await get_current_user(message)
    lang = get_user_lang(user)

    if len(comment) > 500:
        await message.answer(get_label(lang, "comment_too_long"))
        return

    if not user:
        await state.set_state(AppState.main)
        await message.answer(get_label("ru", "user_not_found_error"))
        return

    await add_movie(user[0], title, type_, comment)
    await message.answer(get_label(lang, "ok"))

    await state.clear()
    await state.set_state(AppState.movies_menu)
    await message.answer(get_label(lang, "movies_section"), reply_markup=get_movies_inline_menu(lang))


@router.callback_query(AppState.add_movie_comment, F.data == "skip_movie_comment")
async def skip_movie_comment(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    title = data.get("title")
    type_ = data.get("type_")

    user = await get_current_user(callback)
    lang = get_user_lang(user)

    if not user:
        await state.set_state(AppState.main)
        await callback.message.answer(get_label("ru", "user_not_found_error"))
        await callback.answer()
        return

    await add_movie(user[0], title, type_, "")
    await callback.answer()

    await state.clear()
    await state.set_state(AppState.movies_menu)
    await callback.message.edit_text(get_label(lang, "movies_section"), reply_markup=get_movies_inline_menu(lang))


@router.callback_query(AppState.movies_menu, F.data == "movies:list")
async def list_movies_handler(callback: CallbackQuery, state: FSMContext):
    user = await get_current_user(callback)
    if not user:
        await callback.answer(get_label("ru", "user_not_found_error"))
        return
    await render_movies_list(callback, state, user[0])
    await callback.answer()


@router.callback_query(AppState.movies_menu, F.data == "delete_movie")
async def delete_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.delete_movie_number)
    user = await get_current_user(callback)
    lang = get_user_lang(user)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_label(lang, "cancel_delete"), callback_data="cancel_delete_movie")]
        ]
    )
    await callback.message.answer(get_label(lang, "enter_number_to_delete"), reply_markup=keyboard)
    await callback.answer()


@router.message(AppState.delete_movie_number)
async def delete_by_number(message: Message, state: FSMContext):
    user = await get_current_user(message)
    lang = get_user_lang(user)
    data = await state.get_data()
    movie_map = data.get("movie_map")

    if not movie_map:
        await message.answer(get_label(lang, "first_use_list_movies"))
        await state.set_state(AppState.movies_menu)
        return

    try:
        number = int(message.text)
    except (TypeError, ValueError):
        await message.answer(get_label(lang, "enter_valid_number"))
        return

    if number not in movie_map:
        await message.answer(get_label(lang, "no_movie_with_number"))
        return

    if not user:
        await state.set_state(AppState.main)
        await message.answer(get_label("ru", "user_not_found_error"))
        return

    movie_id = movie_map[number]
    await delete_movie(user[0], movie_id)
    await state.set_state(AppState.movies_menu)
    await render_movies_list(message, state, user[0])


@router.callback_query(AppState.movies_menu, F.data == "menu:main")
async def back_handler(callback: CallbackQuery, state: FSMContext):
    await show_main_menu(callback, state)
    await callback.answer()


@router.callback_query(F.data.startswith("del_movie_"))
async def delete_callback(callback: CallbackQuery, state: FSMContext):
    movie_id = int(callback.data.split("_")[2])
    user = await get_current_user(callback)
    if not user:
        await callback.answer(get_label("ru", "user_not_found_error"))
        return

    await delete_movie(user[0], movie_id)
    await render_movies_list(callback, state, user_id=user[0])
    await callback.answer()


@router.callback_query(AppState.delete_movie_number, F.data == "cancel_delete_movie")
async def cancel_delete_movie(callback: CallbackQuery, state: FSMContext):
    user = await get_current_user(callback)
    if not user:
        await callback.answer(get_label("ru", "user_not_found_error"))
        return

    await state.set_state(AppState.movies_menu)
    await render_movies_list(callback, state, user[0])
    await callback.answer()


async def render_movies_list(event, state, user_id: int):
    user = await get_current_user(event)
    lang = get_user_lang(user)
    movies = await get_movies(user_id)
    if not movies:
        if state:
            await state.update_data(movie_map={})
            await state.set_state(AppState.movies_menu)

        if isinstance(event, CallbackQuery):
            await event.message.edit_text(get_label(lang, "movies_section"), reply_markup=get_movies_inline_menu(lang))
        else:
            await event.answer(get_label(lang, "movies_section"), reply_markup=get_movies_inline_menu(lang))
        return

    text = get_label(lang, "movies_list_title")
    movie_map = {}

    for index, movie in enumerate(movies, start=1):
        movie_id = movie[0]
        title = movie[2]
        type_ = movie[3]
        comment = movie[4]
        comment_text = comment or ""
        text += f"{index}. {title} ({type_}) - {comment_text}\n"
        movie_map[index] = movie_id

    if state:
        await state.update_data(movie_map=movie_map)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_label(lang, "delete"), callback_data="delete_movie")],
            [InlineKeyboardButton(text=get_label(lang, "back"), callback_data="menu:movies")],
        ]
    )

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=keyboard)
    else:
        await event.answer(text, reply_markup=keyboard)
