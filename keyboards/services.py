from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.menu import get_label

#KEYBOARDS---------------------------------------------------------------------------------

def get_services_keyboard(lang="ru"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_label(lang, "add_service"), callback_data="add_service")],
            [InlineKeyboardButton(text=get_label(lang, "delete_service"), callback_data="del_service_")],
            [InlineKeyboardButton(text=get_label(lang, "back"), callback_data="back_mail_list")],
        ]
    )
