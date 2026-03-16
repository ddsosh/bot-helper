from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from database import get_mail, get_services_by_mail, add_service, add_mail, delete_service, delete_mail
from forms.app_states import AppState
from handlers.auth import get_current_user
from keyboards.menu import get_main_reply_menu, get_main_reply_cabinet
from keyboards.services import get_services_keyboard

router = Router()

#USER-----------------------------------------------------------------------------------

async def require_user(event):
    user = await get_current_user(event)

    if not user:

        if isinstance(event, CallbackQuery):
            await event.message.answer("User not found. /start")

        if isinstance(event, Message):
            await event.answer("User not found. /start")

        return None

    return user

#MENU--------------------------------------------------------------------------------------
@router.message(AppState.main, F.text.lower() == "cabinet")
async def cabinet_handler(message: Message, state: FSMContext):
    await state.set_state(AppState.cabinet_menu)
    await message.answer("Cabinet", reply_markup=get_main_reply_cabinet())


@router.callback_query(AppState.cabinet_menu, F.data == "mail")
async def cabinet_callback_query(callback: CallbackQuery, state: FSMContext):
    user = await require_user(callback)

    if not user:
        return

    await render_mail_list(callback, state)

@router.callback_query(AppState.mail_list, F.data.startswith("mail_"))
async def mail_list(callback: CallbackQuery, state: FSMContext):
    mail_id = int(callback.data.split("_")[1])
    await render_services(callback, state, mail_id)

#RENDER-------------------------------------------------------------------------------------------

async def render_mail_list(event, state: FSMContext):
    user = await require_user(event)

    if not user:
        return

    mails = await get_mail(user[0])

    keyboard_buttons = []

    if mails:
        for mail in mails:
            mail_id = mail[0]
            email = mail[2]
            keyboard_buttons.append(
                [InlineKeyboardButton(text=email, callback_data=f"mail_{mail_id}")]
            )

    keyboard_buttons.append(
        [InlineKeyboardButton(text="Add mail", callback_data="add_mail")]
    )
    keyboard_buttons.append(
        [InlineKeyboardButton(text="Del mail", callback_data="del_mail")]
    )
    keyboard_buttons.append(
        [InlineKeyboardButton(text="Back", callback_data="back_cabinet")]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    text = "Mail:\n"

    if not mails:
        text += "No mails yet"

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=keyboard)
    elif isinstance(event, Message):
        await event.answer(text, reply_markup=keyboard)

    await state.set_state(AppState.mail_list)

async def render_services(event, state: FSMContext, mail_id: int):
    user = await require_user(event)

    if not user:
        return

    services = await get_services_by_mail(user[0], mail_id)

    keyboard = get_services_keyboard()

    text = format_services(services)

    if isinstance(event, CallbackQuery):

        msg = await event.message.edit_text(text, reply_markup=keyboard)

        await state.update_data(
            current_mail_id=mail_id,
            services_message_id=msg.message_id
        )

        await event.answer()

    else:

        msg = await event.answer(text, reply_markup=keyboard)

        await state.update_data(
            current_mail_id=mail_id,
            services_message_id=msg.message_id
        )

#ADD SERVICE-------------------------------------------------------------------------------------------

@router.callback_query(AppState.mail_list, F.data == "add_service")
async def add_service_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.add_service_name)
    await callback.message.answer("Service name", reply_markup=ReplyKeyboardRemove())
    await callback.answer()

@router.message(AppState.add_service_name)
async def add_service_name(message: Message, state: FSMContext):
    service_name = (message.text or "").strip()

    if not service_name:
        await message.answer("Title cannot be empty")
        return

    if len(service_name) > 50:
        await message.answer("Title is too long (max 50)")
        return

    await state.update_data(service_name=service_name)
    await state.set_state(AppState.add_service_login)
    await message.answer("Service login", reply_markup=ReplyKeyboardRemove())

@router.message(AppState.add_service_login)
async def add_service_login (message: Message, state: FSMContext):
    login = (message.text or "").strip()

    if not login:
        await message.answer("Title cannot be empty")
        return

    if len(login) > 50:
        await message.answer("Title is too long (max 50)")
        return

    await state.update_data(login=login)
    await state.set_state(AppState.add_service_comment)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Skip", callback_data="skip_service_comm")]]
    )
    await message.answer("Service comment or Skip", reply_markup=keyboard)

@router.message(AppState.add_service_comment)
async def add_service_comment (message: Message, state: FSMContext):

    data = await state.get_data()
    mail_id = data["current_mail_id"]
    service_name = data["service_name"]
    login = data["login"]

    comment = (message.text or "").strip()

    if len(comment) > 500:
        await message.answer("Comment is too long (max 500)")
        return

    user = await require_user(message)

    if not user:
        return

    created = await add_service(user[0], mail_id, service_name, login, comment)
    if not created:
        await message.answer("Mail not found. /start")
        await state.set_state(AppState.main)
        return

    await state.set_state(AppState.mail_list)
    await render_services(message, state, mail_id)

@router.callback_query(AppState.add_service_comment, F.data == "skip_service_comm")
async def skip_service_comment(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mail_id = data["current_mail_id"]
    service_name = data["service_name"]
    login = data["login"]

    user = await require_user(callback)

    if not user:
        await state.set_state(AppState.main)
        await callback.message.answer("error(user not found) /start", reply_markup=get_main_reply_menu())
        await callback.answer()
        return

    created = await add_service(user[0], mail_id, service_name, login, None)
    if not created:
        await state.set_state(AppState.main)
        await callback.message.answer("Mail not found. /start", reply_markup=get_main_reply_menu())
        await callback.answer()
        return
    await callback.answer("OK service saved without comment")

    await state.set_state(AppState.mail_list)
    await render_services(callback, state, mail_id)

#BACK-------------------------------------------------------------------------------------------

@router.callback_query(AppState.mail_list, F.data == "back_mail_list")
async def back_handler(callback: CallbackQuery, state: FSMContext):
    await render_mail_list(callback, state)

@router.message(AppState.cabinet_menu, F.text.lower() == "back")
async def back_handler(message: Message, state: FSMContext):
    await state.set_state(AppState.main)
    await message.answer("Main menu", reply_markup=get_main_reply_menu())

@router.callback_query(F.data == "back_services")
async def back_to_services(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    mail_id = data["current_mail_id"]

    await render_services(callback, state, mail_id)

@router.callback_query(AppState.mail_list, F.data == "back_cabinet")
async def back_to_cabinet(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.cabinet_menu)
    await callback.message.edit_text("Cabinet", reply_markup=get_main_reply_cabinet())
    await callback.answer()

#FORM SERV-------------------------------------------------------------------------------------------

def format_services(services):

    text = "Services:\n"

    if services:
        for index, service in enumerate(services, start=1):
            service_id = service[0]
            service_name = service[2]
            comment = service[4]

            comment_text = comment if comment else "No comment"

            text += f"{index}. {service_name} - {comment_text}\n"

    else:
        text += "No services yet"

    return text

#ADD MAIL-------------------------------------------------------------------------------------------

@router.callback_query(AppState.mail_list, F.data == "add_mail")
async def add_mail_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.add_mail)
    await callback.message.answer("Mail name", reply_markup=ReplyKeyboardRemove())
    await callback.answer()


@router.message(AppState.add_mail)
async def add_mail_name(message: Message, state: FSMContext):
    email = (message.text or "").strip()

    if not email:
        await message.answer("Mail cannot be empty")
        return

    if len(email) > 50:
        await message.answer("Mail is too long (max 50)")
        return

    user = await require_user(message)

    if not user:
        return

    await add_mail(user[0], email)
    await state.set_state(AppState.mail_list)
    await render_mail_list(message, state)

#DEL SERVICE-------------------------------------------------------------------------------------------

@router.callback_query(AppState.mail_list, F.data == "del_service_")
async def delete_service_mode(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mail_id = data["current_mail_id"]

    user = await require_user(callback)

    if not user:
        return

    services = await get_services_by_mail(user[0], mail_id)

    if not services:
        await callback.answer("if not services:")
        return

    keyboard_buttons = []

    for service in services:
        service_id = service[0]
        service_name = service[2]

        keyboard_buttons.append(
            [InlineKeyboardButton(
                text=f"Delete {service_name}",
                callback_data=f"delete_service_{service_id}"
            )]
        )

    keyboard_buttons.append(
        [InlineKeyboardButton(text="Back", callback_data="back_services")]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await callback.message.edit_text("Select service to delete:", reply_markup=keyboard)
    await callback.answer()

@router.callback_query(AppState.mail_list, F.data.startswith("delete_service_"))
async def delete_service_handler(callback: CallbackQuery, state: FSMContext):

    service_id = int(callback.data.split("_")[2])

    data = await state.get_data()
    mail_id = data["current_mail_id"]

    user = await require_user(callback)

    if not user:
        return

    await delete_service(user[0], service_id)
    await callback.answer("Service deleted")
    await render_services(callback, state, mail_id)

#DEL MAIL-------------------------------------------------------------------------------------------

@router.callback_query(AppState.mail_list, F.data == "del_mail")
async def delete_mail_mode(callback: CallbackQuery, state: FSMContext):
    user = await require_user(callback)

    if not user:
        return

    mails = await get_mail(user[0])

    if not mails:
        await callback.answer("No mails found")
        return

    keyboard_buttons = []

    for mail_id, user_id, email in mails:

        keyboard_buttons.append(
            [InlineKeyboardButton(
                text=f"Delete {email}",
                callback_data=f"delete_mail_{mail_id}"
            )]
        )

    keyboard_buttons.append(
        [InlineKeyboardButton(text="Back", callback_data="back_mail_list")]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await callback.message.edit_text("Select mail to delete:", reply_markup=keyboard)
    await callback.answer()

@router.callback_query(AppState.mail_list, F.data.startswith("delete_mail_"))
async def delete_mail_handler(callback: CallbackQuery, state: FSMContext):
    mail_id = int(callback.data.split("_")[-1])
    user = await require_user(callback)

    if not user:
        return

    await delete_mail(user[0], mail_id)
    await callback.answer("Mail deleted")
    await render_mail_list(callback, state)

async def send_or_edit(event, text, keyboard):
    msg = None
    if isinstance(event, CallbackQuery):
        msg = await event.message.edit_text(text, reply_markup=keyboard)
        await event.answer()

    elif isinstance(event, Message):
        msg = await event.answer(text, reply_markup=keyboard)

    return msg

