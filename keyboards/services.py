from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#KEYBOARDS---------------------------------------------------------------------------------

def get_services_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="add service", callback_data="add_service")],
            [InlineKeyboardButton(text="del service", callback_data="del_service_")],
            [InlineKeyboardButton(text="back", callback_data="back_mail_list")],
        ]
    )
