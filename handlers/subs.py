from datetime import datetime

import aiosqlite
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from dateutil.relativedelta import relativedelta

from database import add_subscription, get_subscriptions, delete_subscription, DB_NAME
from forms.app_states import AppState
from handlers.auth import get_current_user, get_user_lang
from keyboards.menu import get_subs_inline_menu, get_label
from handlers.session import show_main_menu

router = Router()


@router.callback_query(F.data == "menu:subs")
async def main_message(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.subs_menu)
    user = await get_current_user(callback)
    lang = get_user_lang(user)
    await callback.message.edit_text(get_label(lang, "subs_section"), reply_markup=get_subs_inline_menu(lang))
    await callback.answer()


@router.callback_query(AppState.subs_menu, F.data == "subs:add")
async def main_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.add_subscription_title)
    user = await get_current_user(callback)
    await callback.message.edit_text(get_label(get_user_lang(user), "enter_title"))
    await callback.answer()


@router.message(AppState.add_subscription_title)
async def subs_title(message: Message, state: FSMContext):
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
    await state.set_state(AppState.add_subscription_price)
    await message.answer(get_label(lang, "enter_price"), reply_markup=ReplyKeyboardRemove())


@router.message(AppState.add_subscription_price)
async def subs_price(message: Message, state: FSMContext):
    user = await get_current_user(message)
    lang = get_user_lang(user)
    text = (message.text or "").strip()

    if not text:
        await message.answer(get_label(lang, "price_empty"))
        return
    try:
        price = int(text)
    except ValueError:
        await message.answer(get_label(lang, "invalid_price"))
        return

    await state.update_data(price=price)
    await state.set_state(AppState.add_subscription_end_date)
    await message.answer(get_label(lang, "enter_end_date"), reply_markup=ReplyKeyboardRemove())


@router.message(AppState.add_subscription_end_date)
async def subs_end_date(message: Message, state: FSMContext):
    user = await get_current_user(message)
    lang = get_user_lang(user)
    end_date = (message.text or "").strip()

    if not end_date:
        await message.answer(get_label(lang, "end_date_empty"))
        return

    try:
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        await message.answer(get_label(lang, "wrong_date_format"))
        return

    await state.update_data(end_date=end_date)
    await state.set_state(AppState.add_subscription_comment)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=get_label(lang, "skip"), callback_data="skip_sub_comm")]]
    )
    await message.answer(get_label(lang, "enter_comment_or_skip"), reply_markup=keyboard)


@router.message(AppState.add_subscription_comment)
async def subs_comment(message: Message, state: FSMContext):
    data = await state.get_data()
    title = data.get("title")
    price = data.get("price")
    end_date = data.get("end_date")
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

    await add_subscription(user[0], title, price, end_date, comment)
    await message.answer(get_label(lang, "ok"))

    await state.clear()
    await state.set_state(AppState.subs_menu)
    await message.answer(get_label(lang, "subs_section"), reply_markup=get_subs_inline_menu(lang))


@router.callback_query(AppState.add_subscription_comment, F.data == "skip_sub_comm")
async def skip_subs_comment(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    title = data.get("title")
    price = data.get("price")
    end_date = data.get("end_date")

    user = await get_current_user(callback)
    lang = get_user_lang(user)

    if not user:
        await state.set_state(AppState.main)
        await callback.message.answer(get_label("ru", "user_not_found_error"))
        await callback.answer()
        return

    await add_subscription(user[0], title, price, end_date, None)
    await callback.answer()

    await state.clear()
    await state.set_state(AppState.subs_menu)
    await callback.message.edit_text(get_label(lang, "subs_section"), reply_markup=get_subs_inline_menu(lang))


@router.callback_query(AppState.subs_menu, F.data == "subs:list")
async def list_note_handler(callback: CallbackQuery, state: FSMContext):
    user = await get_current_user(callback)
    if not user:
        await callback.answer(get_label("ru", "user_not_found_error"))
        return
    await render_subs_list(callback, state, user[0])
    await callback.answer()


@router.callback_query(AppState.subs_menu, F.data == "extend_sub")
async def extend_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.extend_subscription_number)
    user = await get_current_user(callback)
    lang = get_user_lang(user)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_label(lang, "cancel"), callback_data="cancel_extend_sub")]
        ]
    )
    await callback.message.edit_text(get_label(lang, "enter_sub_number"), reply_markup=keyboard)
    await callback.answer()


@router.callback_query(AppState.subs_menu, F.data == "delete_sub")
async def delete_sub_start_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.delete_subscription_number)
    user = await get_current_user(callback)
    lang = get_user_lang(user)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_label(lang, "cancel_delete"), callback_data="cancel_delete_sub")]
        ]
    )
    await callback.message.edit_text(get_label(lang, "enter_number"), reply_markup=keyboard)
    await callback.answer()


@router.message(AppState.extend_subscription_number)
async def get_number(message: Message, state: FSMContext):
    user = await get_current_user(message)
    lang = get_user_lang(user)
    data = await state.get_data()
    sub_map = data.get("sub_map")

    if not sub_map:
        await message.answer(get_label(lang, "first_use_list_subs"))
        await state.set_state(AppState.subs_menu)
        return

    if not message.text.isdigit():
        await message.answer(get_label(lang, "enter_valid_number"))
        return

    number = int(message.text)

    if number not in sub_map:
        await message.answer(get_label(lang, "invalid_number"))
        return

    subscription_id = sub_map[number]
    await state.update_data(subscription_id=subscription_id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=get_label(lang, "one_month"), callback_data="extend_1"),
                InlineKeyboardButton(text=get_label(lang, "three_months"), callback_data="extend_3"),
            ],
            [
                InlineKeyboardButton(text=get_label(lang, "six_months"), callback_data="extend_6"),
                InlineKeyboardButton(text=get_label(lang, "other"), callback_data="extend_other"),
            ],
            [
                InlineKeyboardButton(text=get_label(lang, "back"), callback_data="back_list_number"),
            ],
        ]
    )

    await state.set_state(AppState.extend_subscription_period)
    await message.answer(get_label(lang, "choose_period"), reply_markup=keyboard)


@router.callback_query(AppState.extend_subscription_period, F.data.startswith("extend_"))
async def process_extension(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    subscription_id = data.get("subscription_id")
    user = await get_current_user(callback)
    lang = get_user_lang(user)

    months_map = {
        "extend_1": 1,
        "extend_3": 3,
        "extend_6": 6,
    }

    if callback.data == "extend_other":
        await state.set_state(AppState.extend_custom_months)
        await callback.message.answer(get_label(lang, "enter_months_number"), reply_markup=ReplyKeyboardRemove())
        await callback.answer()
        return

    months = months_map.get(callback.data)
    if months is None:
        await callback.answer()
        return

    success = await extend_subscription_date(subscription_id, months)
    if not success:
        await callback.message.answer(get_label(lang, "subscription_not_found"))
        await state.set_state(AppState.subs_menu)
        await callback.answer()
        return

    await callback.message.answer(get_label(lang, "subscription_extended"), reply_markup=get_subs_inline_menu(lang))
    await state.set_state(AppState.subs_menu)
    await callback.answer()


async def extend_subscription_date(subscription_id, months):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT end_date FROM subscriptions WHERE id = ?
            """,
            (subscription_id,),
        )

        result = await cursor.fetchone()

        if not result:
            return False

        end_date_str = result[0]
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        if end_date < datetime.now():
            base_date = datetime.now()
        else:
            base_date = end_date

        new_date = base_date + relativedelta(months=months)

        await db.execute(
            """
            UPDATE subscriptions
            SET end_date = ?, 
                reminded_5_days = 0,
                reminded_1_day = 0
            WHERE id = ?
            """,
            (new_date.strftime("%Y-%m-%d"), subscription_id),
        )

        await db.commit()
        return True


@router.message(AppState.extend_custom_months)
async def process_custom_months(message: Message, state: FSMContext):
    user = await get_current_user(message)
    lang = get_user_lang(user)

    if not message.text.isdigit():
        await message.answer(get_label(lang, "enter_valid_number"))
        return

    months = int(message.text)
    data = await state.get_data()
    subscription_id = data.get("subscription_id")

    if not subscription_id:
        await message.answer(get_label(lang, "error_start_again"))
        await state.set_state(AppState.subs_menu)
        return

    await extend_subscription_date(subscription_id, months)
    await message.answer(get_label(lang, "subscription_extended"), reply_markup=get_subs_inline_menu(lang))
    await state.set_state(AppState.subs_menu)


@router.callback_query(AppState.extend_subscription_period, F.data == "back_list_number")
async def back_list_number(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.extend_subscription_number)
    user = await get_current_user(callback)
    await callback.message.answer(get_label(get_user_lang(user), "enter_sub_number"))
    await callback.answer()


@router.message(AppState.delete_subscription_number)
async def delete_sub_by_number(message: Message, state: FSMContext):
    user = await get_current_user(message)
    lang = get_user_lang(user)
    data = await state.get_data()
    sub_map = data.get("sub_map")

    if not sub_map:
        await message.answer(get_label(lang, "first_use_list_subs"))
        await state.set_state(AppState.subs_menu)
        return

    try:
        number = int(message.text)
    except (TypeError, ValueError):
        await message.answer(get_label(lang, "enter_valid_number"))
        return

    if number not in sub_map:
        await message.answer(get_label(lang, "no_sub_with_number"))
        return

    if not user:
        await state.set_state(AppState.main)
        await message.answer(get_label("ru", "user_not_found_error"))
        return

    sub_id = sub_map[number]
    await delete_subscription(user[0], sub_id)
    await state.set_state(AppState.subs_menu)
    await render_subs_list(message, state, user[0])


@router.callback_query(F.data.startswith("del_sub_"))
async def delete_callback(callback: CallbackQuery, state: FSMContext):
    sub_id = int(callback.data.split("_")[2])
    user = await get_current_user(callback)

    if not user:
        await callback.answer(get_label("ru", "user_not_found_error"))
        return

    await delete_subscription(user[0], sub_id)
    await render_subs_list(callback, state, user_id=user[0])
    await callback.answer()


@router.callback_query(AppState.delete_subscription_number, F.data == "cancel_delete_sub")
async def cancel_delete_sub(callback: CallbackQuery, state: FSMContext):
    user = await get_current_user(callback)
    if not user:
        await callback.answer(get_label("ru", "user_not_found_error"))
        return

    await state.set_state(AppState.subs_menu)
    await render_subs_list(callback, state, user[0])
    await callback.answer()


@router.callback_query(AppState.extend_subscription_number, F.data == "cancel_extend_sub")
async def cancel_extend_sub(callback: CallbackQuery, state: FSMContext):
    user = await get_current_user(callback)
    if not user:
        await callback.answer(get_label("ru", "user_not_found_error"))
        return

    await state.set_state(AppState.subs_menu)
    await render_subs_list(callback, state, user[0])
    await callback.answer()


async def render_subs_list(event, state, user_id: int):
    user = await get_current_user(event)
    lang = get_user_lang(user)
    subs = await get_subscriptions(user_id)
    if not subs:
        if state:
            await state.update_data(sub_map={})
            await state.set_state(AppState.subs_menu)

        if isinstance(event, CallbackQuery):
            await event.message.edit_text(get_label(lang, "subs_section"), reply_markup=get_subs_inline_menu(lang))
        else:
            await event.answer(get_label(lang, "subs_section"), reply_markup=get_subs_inline_menu(lang))
        return

    text = get_label(lang, "subs_list_title")
    sub_map = {}

    for index, sub in enumerate(subs, start=1):
        sub_id = sub[0]
        title = sub[2]
        price = sub[3]
        end_date = sub[4]
        comment = sub[7]
        comment_text = comment or ""
        text += f"{index}. {title}, {price}, {end_date} - {comment_text}\n"
        sub_map[index] = sub_id

    if state:
        await state.update_data(sub_map=sub_map)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_label(lang, "extend"), callback_data="extend_sub")],
            [InlineKeyboardButton(text=get_label(lang, "delete"), callback_data="delete_sub")],
            [InlineKeyboardButton(text=get_label(lang, "back"), callback_data="menu:subs")],
        ]
    )

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=keyboard)
    else:
        await event.answer(text, reply_markup=keyboard)


@router.callback_query(AppState.subs_menu, F.data == "menu:main")
async def back_handler(callback: CallbackQuery, state: FSMContext):
    await show_main_menu(callback, state)
    await callback.answer()
