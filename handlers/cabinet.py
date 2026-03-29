from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from database import get_mail, get_services_by_mail, add_service, add_mail, delete_service, delete_mail
from forms.app_states import AppState
from handlers.auth import get_current_user, get_user_lang
from keyboards.menu import get_cabinet_inline_menu, get_label
from handlers.session import show_main_menu
from keyboards.services import get_services_keyboard

router = Router()


async def require_user(event):
    user = await get_current_user(event)

    if not user:
        if isinstance(event, CallbackQuery):
            await event.message.answer(get_label("ru", "user_not_found"))
            await event.answer()

        if isinstance(event, Message):
            await event.answer(get_label("ru", "user_not_found"))

        return None

    return user


@router.callback_query(F.data == "menu:cabinet")
async def cabinet_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.cabinet_menu)
    user = await get_current_user(callback)
    lang = get_user_lang(user)
    await callback.message.edit_text(get_label(lang, "cabinet_section"), reply_markup=get_cabinet_inline_menu(lang))
    await callback.answer()


@router.callback_query(AppState.cabinet_menu, F.data == "cabinet:mail")
async def cabinet_message(callback: CallbackQuery, state: FSMContext):
    user = await require_user(callback)
    if not user:
        return
    await render_mail_list(callback, state)
    await callback.answer()


@router.callback_query(AppState.mail_list, F.data.startswith("mail_"))
async def mail_list(callback: CallbackQuery, state: FSMContext):
    mail_id = int(callback.data.split("_")[1])
    await render_services(callback, state, mail_id)


async def render_mail_list(event, state: FSMContext):
    user = await require_user(event)
    if not user:
        return

    lang = get_user_lang(user)
    mails = await get_mail(user[0])

    keyboard_buttons = []

    if mails:
        for mail in mails:
            mail_id = mail[0]
            email = mail[2]
            keyboard_buttons.append([InlineKeyboardButton(text=email, callback_data=f"mail_{mail_id}")])

    keyboard_buttons.append([InlineKeyboardButton(text=get_label(lang, "add_mail"), callback_data="add_mail")])
    keyboard_buttons.append([InlineKeyboardButton(text=get_label(lang, "delete_mail"), callback_data="del_mail")])
    keyboard_buttons.append([InlineKeyboardButton(text=get_label(lang, "back"), callback_data="back_cabinet")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    text = get_label(lang, "mail_list_title")

    if not mails:
        text += get_label(lang, "no_mails_yet")

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=keyboard)
    elif isinstance(event, Message):
        await event.answer(text, reply_markup=keyboard)

    await state.set_state(AppState.mail_list)


async def render_services(event, state: FSMContext, mail_id: int):
    user = await require_user(event)
    if not user:
        return

    lang = get_user_lang(user)
    services = await get_services_by_mail(user[0], mail_id)
    keyboard = get_services_keyboard(lang)
    text = format_services(services, lang)

    if isinstance(event, CallbackQuery):
        msg = await event.message.edit_text(text, reply_markup=keyboard)
        await state.update_data(current_mail_id=mail_id, services_message_id=msg.message_id)
        await event.answer()
    else:
        msg = await event.answer(text, reply_markup=keyboard)
        await state.update_data(current_mail_id=mail_id, services_message_id=msg.message_id)


@router.callback_query(AppState.mail_list, F.data == "add_service")
async def add_service_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.add_service_name)
    user = await get_current_user(callback)
    await callback.message.answer(get_label(get_user_lang(user), "service_name"), reply_markup=ReplyKeyboardRemove())
    await callback.answer()


@router.message(AppState.add_service_name)
async def add_service_name(message: Message, state: FSMContext):
    user = await get_current_user(message)
    lang = get_user_lang(user)
    service_name = (message.text or "").strip()

    if not service_name:
        await message.answer(get_label(lang, "title_empty"))
        return

    if len(service_name) > 50:
        await message.answer(get_label(lang, "title_too_long"))
        return

    await state.update_data(service_name=service_name)
    await state.set_state(AppState.add_service_login)
    await message.answer(get_label(lang, "service_login"), reply_markup=ReplyKeyboardRemove())


@router.message(AppState.add_service_login)
async def add_service_login(message: Message, state: FSMContext):
    user = await get_current_user(message)
    lang = get_user_lang(user)
    login = (message.text or "").strip()

    if not login:
        await message.answer(get_label(lang, "title_empty"))
        return

    if len(login) > 50:
        await message.answer(get_label(lang, "title_too_long"))
        return

    await state.update_data(login=login)
    await state.set_state(AppState.add_service_comment)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=get_label(lang, "skip"), callback_data="skip_service_comm")]]
    )
    await message.answer(get_label(lang, "service_comment_or_skip"), reply_markup=keyboard)


@router.message(AppState.add_service_comment)
async def add_service_comment(message: Message, state: FSMContext):
    data = await state.get_data()
    mail_id = data["current_mail_id"]
    service_name = data["service_name"]
    login = data["login"]
    comment = (message.text or "").strip()

    user = await require_user(message)
    if not user:
        return

    lang = get_user_lang(user)
    if len(comment) > 500:
        await message.answer(get_label(lang, "comment_too_long"))
        return

    created = await add_service(user[0], mail_id, service_name, login, comment)
    if not created:
        await message.answer(get_label(lang, "mail_not_found"))
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
        await callback.message.answer(get_label("ru", "user_not_found_error"))
        await callback.answer()
        return

    lang = get_user_lang(user)
    created = await add_service(user[0], mail_id, service_name, login, None)
    if not created:
        await state.set_state(AppState.main)
        await callback.message.answer(get_label(lang, "mail_not_found"))
        await callback.answer()
        return

    await callback.answer(get_label(lang, "service_saved_without_comment"))
    await state.set_state(AppState.mail_list)
    await render_services(callback, state, mail_id)


@router.callback_query(AppState.mail_list, F.data == "back_mail_list")
async def back_handler(callback: CallbackQuery, state: FSMContext):
    await render_mail_list(callback, state)


@router.callback_query(AppState.cabinet_menu, F.data == "menu:main")
async def back_handler_main(callback: CallbackQuery, state: FSMContext):
    await show_main_menu(callback, state)
    await callback.answer()


@router.callback_query(AppState.mail_list, F.data == "back_services")
async def back_to_services(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mail_id = data["current_mail_id"]
    await render_services(callback, state, mail_id)


@router.callback_query(AppState.mail_list, F.data == "back_cabinet")
async def back_to_cabinet(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.cabinet_menu)
    user = await get_current_user(callback)
    lang = get_user_lang(user)
    await callback.message.edit_text(get_label(lang, "cabinet_section"), reply_markup=get_cabinet_inline_menu(lang))
    await callback.answer()


def format_services(services, lang):
    text = get_label(lang, "services_title")

    if services:
        for index, service in enumerate(services, start=1):
            service_name = service[2]
            comment = service[4]
            comment_text = comment or ""
            text += f"{index}. {service_name} - {comment_text}\n"
    else:
        text += get_label(lang, "no_services_yet")

    return text


@router.callback_query(AppState.mail_list, F.data == "add_mail")
async def add_mail_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.add_mail)
    user = await get_current_user(callback)
    await callback.message.answer(get_label(get_user_lang(user), "mail_name"), reply_markup=ReplyKeyboardRemove())
    await callback.answer()


@router.message(AppState.add_mail)
async def add_mail_name(message: Message, state: FSMContext):
    user = await require_user(message)
    if not user:
        return

    lang = get_user_lang(user)
    email = (message.text or "").strip()

    if not email:
        await message.answer(get_label(lang, "title_empty"))
        return

    if len(email) > 50:
        await message.answer(get_label(lang, "title_too_long"))
        return

    await add_mail(user[0], email)
    await state.set_state(AppState.mail_list)
    await render_mail_list(message, state)


@router.callback_query(AppState.mail_list, F.data == "del_service_")
async def delete_service_mode(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mail_id = data["current_mail_id"]

    user = await require_user(callback)
    if not user:
        return

    lang = get_user_lang(user)
    services = await get_services_by_mail(user[0], mail_id)

    if not services:
        await callback.answer(get_label(lang, "no_services_found"))
        return

    keyboard_buttons = []

    for service in services:
        service_id = service[0]
        service_name = service[2]
        keyboard_buttons.append(
            [InlineKeyboardButton(
                text=get_label(lang, "delete_item", name=service_name),
                callback_data=f"delete_service_{service_id}",
            )]
        )

    keyboard_buttons.append([InlineKeyboardButton(text=get_label(lang, "back"), callback_data="back_services")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await callback.message.edit_text(get_label(lang, "select_service_to_delete"), reply_markup=keyboard)
    await callback.answer()


@router.callback_query(AppState.mail_list, F.data.startswith("delete_service_"))
async def delete_service_handler(callback: CallbackQuery, state: FSMContext):
    service_id = int(callback.data.split("_")[2])
    data = await state.get_data()
    mail_id = data["current_mail_id"]

    user = await require_user(callback)
    if not user:
        return

    lang = get_user_lang(user)
    await delete_service(user[0], service_id)
    await callback.answer(get_label(lang, "service_deleted"))
    await render_services(callback, state, mail_id)


@router.callback_query(AppState.mail_list, F.data == "del_mail")
async def delete_mail_mode(callback: CallbackQuery, state: FSMContext):
    user = await require_user(callback)
    if not user:
        return

    lang = get_user_lang(user)
    mails = await get_mail(user[0])

    if not mails:
        await callback.answer(get_label(lang, "no_mails_found"))
        return

    keyboard_buttons = []

    for mail in mails:
        mail_id = mail[0]
        email = mail[2]
        keyboard_buttons.append(
            [InlineKeyboardButton(
                text=get_label(lang, "delete_item", name=email),
                callback_data=f"delete_mail_{mail_id}",
            )]
        )

    keyboard_buttons.append([InlineKeyboardButton(text=get_label(lang, "back"), callback_data="back_mail_list")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await callback.message.edit_text(get_label(lang, "select_mail_to_delete"), reply_markup=keyboard)
    await callback.answer()


@router.callback_query(AppState.mail_list, F.data.startswith("delete_mail_"))
async def delete_mail_handler(callback: CallbackQuery, state: FSMContext):
    mail_id = int(callback.data.split("_")[-1])
    user = await require_user(callback)
    if not user:
        return

    lang = get_user_lang(user)
    await delete_mail(user[0], mail_id)
    await callback.answer(get_label(lang, "mail_deleted"))
    await render_mail_list(callback, state)


async def send_or_edit(event, text, keyboard):
    msg = None
    if isinstance(event, CallbackQuery):
        msg = await event.message.edit_text(text, reply_markup=keyboard)
        await event.answer()
    elif isinstance(event, Message):
        msg = await event.answer(text, reply_markup=keyboard)
    return msg
