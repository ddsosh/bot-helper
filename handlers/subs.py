from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from datetime import datetime

import aiosqlite
from dateutil.relativedelta import relativedelta
from database import add_subscription, get_subscriptions, delete_subscription, DB_NAME
from forms.app_states import AppState
from handlers.auth import get_current_user
from keyboards.menu import get_subs_inline_menu
from handlers.session import show_main_menu

router = Router()

#MENU--------------------------------------------------------------------------------------

@router.callback_query(F.data == "menu:subs")
async def main_message(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.subs_menu)
    await callback.message.edit_text("Subs Menu", reply_markup=get_subs_inline_menu())
    await callback.answer()



#ADD SUB---------------------------------------------------------------------------------------
@router.callback_query(AppState.subs_menu, F.data == "subs:add")
async def main_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.add_subscription_title)
    await callback.message.edit_text("name")
    await callback.answer()

@router.message(AppState.add_subscription_title)
async def subs_title(message: Message, state: FSMContext):
    title = (message.text or "").strip()

    if not title:
        await message.answer("Title cannot be empty")
        return

    if len(title) > 50:
        await message.answer("Title is too long (max 50)")
        return

    await state.update_data(title=title)
    await state.set_state(AppState.add_subscription_price)
    await message.answer("price", reply_markup=ReplyKeyboardRemove())

@router.message(AppState.add_subscription_price)
async def subs_price(message: Message, state: FSMContext):
    text = (message.text or "").strip()

    if not text:
        await message.answer("Price cannot be empty")
        return
    try:
        price = int(text)
    except ValueError:
        await message.answer("Invalid price")
        return

    await state.update_data(price=price)
    await state.set_state(AppState.add_subscription_end_date)
    await message.answer("end date YYYY-MM-DD", reply_markup=ReplyKeyboardRemove())

@router.message(AppState.add_subscription_end_date)
async def subs_end_date(message: Message, state: FSMContext):
    end_date = (message.text or "").strip()

    if not end_date:
        await message.answer("End date cannot be empty")
        return

    try:
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        await message.answer("Wrong date format. Use YYYY-MM-DD")
        return

    await state.update_data(end_date=end_date)
    await state.set_state(AppState.add_subscription_comment)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⏭️ Skip", callback_data="skip_sub_comm")]]
    )
    await message.answer("Enter comment or Skip", reply_markup=keyboard)


@router.message(AppState.add_subscription_comment)
async def subs_comment(message: Message, state: FSMContext):
    data = await state.get_data()
    title = data.get("title")
    price = data.get("price")
    end_date = data.get("end_date")

    comment = (message.text or "").strip()

    if len(comment) > 500:
        await message.answer("Comment is too long (max 500)")
        return

    user = await get_current_user(message)

    if not user:
        await state.set_state(AppState.main)
        await message.answer("error(user not found) /start")
        return

    await add_subscription(user[0], title, price, end_date, comment)
    await message.answer("OK")

    await state.clear()
    await state.set_state(AppState.subs_menu)
    await message.answer("Subs menu", reply_markup=get_subs_inline_menu())


#SKIP--------------------------------------------------------------------------------------
@router.callback_query(AppState.add_subscription_comment, F.data == "skip_sub_comm")
async def skip_subs_comment(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    title = data.get("title")
    price = data.get("price")
    end_date = data.get("end_date")

    user = await get_current_user(callback)

    if not user:
        await state.set_state(AppState.main)
        await callback.message.answer("error(user not found) /start")
        await callback.answer()
        return

    await add_subscription(user[0], title,  price, end_date,  None)
    await callback.answer()

    await state.clear()
    await state.set_state(AppState.subs_menu)
    await callback.message.edit_text("Subs section", reply_markup=get_subs_inline_menu())


#LIST--------------------------------------------------------------------------------------
@router.callback_query(AppState.subs_menu, F.data == "subs:list")
async def list_note_handler(callback: CallbackQuery, state: FSMContext):
    user = await get_current_user(callback)
    if not user:
        await callback.answer("error(list) /start")
        return
    await render_subs_list(callback, state, user[0])
    await callback.answer()


#EXTEND------------------------------------------------------------------------------------
@router.callback_query(AppState.subs_menu, F.data == "extend_sub")
async def extend_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.extend_subscription_number)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✖️ Cancel", callback_data="cancel_extend_sub")]
        ]
    )
    await callback.message.edit_text("Enter sub num", reply_markup=keyboard)
    await callback.answer()

@router.callback_query(AppState.subs_menu, F.data == "delete_sub")
async def delete_sub_start_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.delete_subscription_number)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✖️ Cancel delete", callback_data="cancel_delete_sub")]
        ]
    )
    await callback.message.edit_text("Enter num", reply_markup=keyboard)
    await callback.answer()

@router.message(AppState.extend_subscription_number)
async def get_number(message: Message, state: FSMContext):
    data = await state.get_data()
    sub_map = data.get("sub_map")

    if not sub_map:
        await message.answer("First use 'list subs'")
        await state.set_state(AppState.subs_menu)
        return

    if not message.text.isdigit():
        await message.answer("Enter valid number")
        return

    number = int(message.text)

    if number not in sub_map:
        await message.answer("Invalid number")
        return

    subscription_id = sub_map[number]

    await state.update_data(subscription_id=subscription_id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1 month", callback_data="extend_1"),
                InlineKeyboardButton(text="3 months", callback_data="extend_3"),
            ],
            [
                InlineKeyboardButton(text="6 months", callback_data="extend_6"),
                InlineKeyboardButton(text="…", callback_data="extend_other"),
            ],
            [
                InlineKeyboardButton(text="⬅️ Back", callback_data="back_list_number"),
            ]
        ]
    )

    await state.set_state(AppState.extend_subscription_period)
    await message.answer("Choose period:", reply_markup=keyboard)

@router.callback_query(AppState.extend_subscription_period, F.data.startswith("extend_"))
async def process_extension(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    subscription_id = data.get("subscription_id")

    months_map = {
        "extend_1": 1,
        "extend_3": 3,
        "extend_6": 6,
    }

    if callback.data == "extend_other":
        await state.set_state(AppState.extend_custom_months)
        await callback.message.answer("Enter number of months:", reply_markup=ReplyKeyboardRemove())
        await callback.answer()
        return

    months = months_map.get(callback.data)

    if months is None:
        await callback.answer()
        return

    success = await extend_subscription_date(subscription_id, months)

    if not success:
        await callback.message.answer("Subscription not found")
        await state.set_state(AppState.subs_menu)
        await callback.answer()
        return

    await callback.message.answer("Subscription extended", reply_markup=get_subs_inline_menu())
    await state.set_state(AppState.subs_menu)
    await callback.answer()

async def extend_subscription_date(subscription_id, months):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
            SELECT end_date FROM subscriptions WHERE id = ?
        """, (subscription_id,))

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

        await db.execute("""
            UPDATE subscriptions
            SET end_date = ?, 
                reminded_5_days = 0,
                reminded_1_day = 0
            WHERE id = ?
        """, (new_date.strftime("%Y-%m-%d"), subscription_id))

        await db.commit()

        return True

@router.message(AppState.extend_custom_months)
async def process_custom_months(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("Enter valid number")
        return

    months = int(message.text)

    data = await state.get_data()
    subscription_id = data.get("subscription_id")

    if not subscription_id:
        await message.answer("Error. Start again")
        await state.set_state(AppState.subs_menu)
        return

    await extend_subscription_date(subscription_id, months)

    await message.answer("Subscription extended", reply_markup=get_subs_inline_menu())
    await state.set_state(AppState.subs_menu)


@router.callback_query(AppState.extend_subscription_period,F.data == "back_list_number")
async def back_list_number(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.extend_subscription_number)
    await callback.message.answer("Enter sub num")
    await callback.answer()


#DELETE------------------------------------------------------------------------------------

@router.message(AppState.delete_subscription_number)
async def delete_sub_by_number(message: Message, state: FSMContext):
    data = await state.get_data()
    sub_map = data.get("sub_map")

    if not sub_map:
        await message.answer("First use 'list subs'")
        await state.set_state(AppState.subs_menu)
        return

    try:
        number = int(message.text)
    except (TypeError, ValueError):
        await message.answer("Enter a valid number")
        return

    if number not in sub_map:
        await message.answer("No sub with that number")
        return

    sub_id = sub_map[number]
    user = await get_current_user(message)
    if not user:
        await state.set_state(AppState.main)
        await message.answer("error(user not found) /start")
        return

    await delete_subscription(user[0], sub_id)
    await state.set_state(AppState.subs_menu)
    await render_subs_list(message, state, user[0])

#DEL SUB CB---------------------------------------------------------------------------------
@router.callback_query(F.data.startswith("del_sub_"))
async def delete_callback(callback: CallbackQuery, state: FSMContext):
    sub_id = int(callback.data.split("_")[2])
    user = await get_current_user(callback)

    if not user:
        await callback.answer("error(user not found) /start")
        return

    await delete_subscription(user[0], sub_id)
    await render_subs_list(callback, state, user_id=user[0])
    await callback.answer()


@router.callback_query(AppState.delete_subscription_number, F.data == "cancel_delete_sub")
async def cancel_delete_sub(callback: CallbackQuery, state: FSMContext):
    user = await get_current_user(callback)
    if not user:
        await callback.answer("error(user not found) /start")
        return

    await state.set_state(AppState.subs_menu)
    await render_subs_list(callback, state, user[0])
    await callback.answer()


@router.callback_query(AppState.extend_subscription_number, F.data == "cancel_extend_sub")
async def cancel_extend_sub(callback: CallbackQuery, state: FSMContext):
    user = await get_current_user(callback)
    if not user:
        await callback.answer("error(user not found) /start")
        return

    await state.set_state(AppState.subs_menu)
    await render_subs_list(callback, state, user[0])
    await callback.answer()


async def render_subs_list(event, state, user_id: int):
    subs = await get_subscriptions(user_id)
    if not subs:
        if isinstance(event, CallbackQuery):
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="⬅️ Back", callback_data="menu:subs")]
                ]
            )
            await event.message.edit_text("list empty", reply_markup=keyboard)
        else:
            await event.answer("list empty")
        return

    text = "Subs:\n"
    sub_map = {}

    for index, sub in enumerate(subs, start=1):
        sub_id, user_id, title, price, end_date, reminded_5_days, reminded_1_day, comment = sub[:8]
        comment_text = comment if comment else "No comment"
        text += f"{index}. {title}, {price}, {end_date} - {comment_text}\n"
        sub_map[index] = sub_id

    if state:
        await state.update_data(sub_map=sub_map)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏳ Extend", callback_data="extend_sub")],
            [InlineKeyboardButton(text="🗑️ Delete", callback_data="delete_sub")],
            [InlineKeyboardButton(text="⬅️ Back", callback_data="menu:subs")],
        ]
    )

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=keyboard)
    else:
        await event.answer(text, reply_markup=keyboard)


#BACK--------------------------------------------------------------------------------------
@router.callback_query(AppState.subs_menu, F.data == "menu:main")
async def back_handler(callback: CallbackQuery, state: FSMContext):
    await show_main_menu(callback, state)
    await callback.answer()
