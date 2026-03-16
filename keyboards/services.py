from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#KEYBOARDS---------------------------------------------------------------------------------

def get_services_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Add service", callback_data="add_service")],
            [InlineKeyboardButton(text="🗑️ Delete service", callback_data="del_service_")],
            [InlineKeyboardButton(text="⬅️ Back", callback_data="back_mail_list")],
        ]
    )
