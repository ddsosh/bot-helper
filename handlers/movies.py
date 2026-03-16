from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext


from keyboards.menu import get_main_reply_movies, get_main_reply_menu
from handlers.auth import get_current_user
from database import get_movies, delete_movie, add_movie
from forms.app_states import AppState


router = Router()

# MENU--------------------------------------------------------------------------------------


@router.message(AppState.main, F.text.lower() == "movies")
async def movies_menu(message: Message, state: FSMContext):
    await state.set_state(AppState.movies_menu)
    await message.answer("Movies section", reply_markup=get_main_reply_movies())


@router.message(AppState.movies_menu, F.text.lower() == "add movie")
async def add_movie_start(message: Message, state: FSMContext):
    await state.set_state(AppState.add_movie_title)
    await message.answer("Enter name", reply_markup=ReplyKeyboardRemove())


#ADD MOVIE---------------------------------------------------------------------------------------
@router.message(AppState.add_movie_title)
async def movie_title(message: Message, state: FSMContext):
    title = (message.text or "").strip()
    if not title:
        await message.answer("Title cannot be empty")
        return
    if len(title) > 50:
        await message.answer("Title is too long (max 50)")
        return

    await state.update_data(title=title)
    await state.set_state(AppState.add_movie_type)
    await message.answer("M | S", reply_markup=ReplyKeyboardRemove())


@router.message(AppState.add_movie_type)
async def movie_type(message: Message, state: FSMContext):
    type_ = (message.text or "").strip().upper()
    if type_ not in {"M", "S"}:
        await message.answer("Type must be 'M' or 'S'")
        return

    await state.update_data(type_=type_)
    await state.set_state(AppState.add_movie_comment)
    await message.answer("comment:", reply_markup=ReplyKeyboardRemove())


@router.message(AppState.add_movie_comment)
async def movie_comment(message: Message, state: FSMContext):
    data = await state.get_data()
    title = data["title"]
    type_ = data["type_"]

    comment = (message.text or "").strip()

    if len(comment) > 500:
        await message.answer("Comment is too long (max 500)")
        return

    user = await get_current_user(message)
    if not user:
        await state.set_state(AppState.main)
        await message.answer("error(user not found) /start", reply_markup=get_main_reply_menu())
        return

    await add_movie(user[0], title, type_, comment)
    await message.answer("OK")

    await state.clear()
    await state.set_state(AppState.movies_menu)
    await message.answer("Movies section", reply_markup=get_main_reply_movies())


#LIST MOVIE--------------------------------------------------------------------------------------
@router.message(AppState.movies_menu, F.text.lower() == "list movies")
async def list_movies_handler(message: Message, state: FSMContext):
    user = await get_current_user(message)
    if not user:
        await message.answer("error(list) /start")
        return
    await render_movies_list(message, state, user[0])


#DELETE MOVIE------------------------------------------------------------------------------------
@router.callback_query(AppState.movies_menu, F.data == "delete_movie")
async def delete_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.delete_movie_number)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="cancel delete", callback_data="cancel_delete_movie")]
        ]
    )
    await callback.message.answer("Enter number to delete:", reply_markup=keyboard)
    await callback.answer()


@router.message(AppState.delete_movie_number)
async def delete_by_number(message: Message, state: FSMContext):
    data = await state.get_data()
    movie_map = data.get("movie_map")

    if not movie_map:
        await message.answer("First use 'list movies'")
        await state.set_state(AppState.movies_menu)
        return

    try:
        number = int(message.text)
    except (TypeError, ValueError):
        await message.answer("Enter a valid number")
        return

    if number not in movie_map:
        await message.answer("No movie with that number")
        return

    movie_id = movie_map[number]
    user = await get_current_user(message)
    if not user:
        await state.set_state(AppState.main)
        await message.answer("error(user not found) /start", reply_markup=get_main_reply_menu())
        return

    await delete_movie(user[0], movie_id)
    await state.set_state(AppState.movies_menu)
    await render_movies_list(message, state, user[0])


#BACK--------------------------------------------------------------------------------------
@router.message(AppState.movies_menu, F.text.lower() == "back")
async def back_handler(message: Message, state: FSMContext):
    await state.set_state(AppState.main)
    await message.answer("Main menu", reply_markup=get_main_reply_menu())


#DEL MOVIE CB---------------------------------------------------------------------------------
@router.callback_query(F.data.startswith("del_movie_"))
async def delete_callback(callback: CallbackQuery):
    movie_id = int(callback.data.split("_")[2])
    user = await get_current_user(callback)
    if not user:
        await callback.answer("error(user not found) /start")
        return

    await delete_movie(user[0], movie_id)
    await render_movies_list(callback, state=None, user_id=user[0])
    await callback.answer()


@router.callback_query(AppState.delete_movie_number, F.data == "cancel_delete_movie")
async def cancel_delete_movie(callback: CallbackQuery, state: FSMContext):
    user = await get_current_user(callback)
    if not user:
        await callback.answer("error(user not found) /start")
        return

    await state.set_state(AppState.movies_menu)
    await render_movies_list(callback, state, user[0])
    await callback.answer()


async def render_movies_list(event, state, user_id: int):
    movies = await get_movies(user_id)
    if not movies:
        if isinstance(event, CallbackQuery):
            await event.message.edit_text("list empty")
        else:
            await event.answer("list empty")
        return

    text = "Movies list:\n\n"
    movie_map = {}

    for index, movie in enumerate(movies, start=1):
        movie_id, user_id, title, type_, comment, created_at = movie
        text += f"{index}. {title} ({type_}) - {comment}\n"
        movie_map[index] = movie_id

    if state:
        await state.update_data(movie_map=movie_map)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="delete", callback_data="delete_movie")]
        ]
    )

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=keyboard)
    else:
        await event.answer(text, reply_markup=keyboard)
