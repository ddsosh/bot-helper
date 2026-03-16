from aiogram import Router
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
router = Router()

#REPLY MENUS-------------------------------------------------------------------------------

def get_main_reply_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="movies"), KeyboardButton(text="notes")],
             [KeyboardButton(text="subs"), KeyboardButton(text="cabinet")],
        ],
        resize_keyboard=True
    )
    return keyboard


def get_main_reply_movies():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="add movie"), KeyboardButton(text="list movies")],
            [KeyboardButton(text="back")],
        ],
        resize_keyboard=True
    )
    return keyboard


def get_main_reply_notes():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="add note"), KeyboardButton(text="list notes")],
            [KeyboardButton(text="back")],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_main_reply_subs():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="add sub"), KeyboardButton(text="list subs")],
            [KeyboardButton(text="back")],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_main_reply_cabinet():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="mail"), KeyboardButton(text="back")],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_main_reply_mail():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="mail"), KeyboardButton(text="back")],
        ],
        resize_keyboard=True
    )
    return keyboard

#INLINE MENUS-------------------------------------------------------------------------------

def get_main_inline_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎬 Movies", callback_data="menu:movies"),
                InlineKeyboardButton(text="📝 Notes", callback_data="menu:notes"),
            ],
            [
                InlineKeyboardButton(text="💳 Subs", callback_data="menu:subs"),
                InlineKeyboardButton(text="🗂️ Cabinet", callback_data="menu:cabinet"),
            ],
        ]
    )


def get_movies_inline_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Add movie", callback_data="movies:add"),
                InlineKeyboardButton(text="📋 List movies", callback_data="movies:list"),
            ],
            [
                InlineKeyboardButton(text="⬅️ Back", callback_data="menu:main"),
            ],
        ]
    )


def get_notes_inline_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Add note", callback_data="notes:add"),
                InlineKeyboardButton(text="📋 List notes", callback_data="notes:list"),
            ],
            [
                InlineKeyboardButton(text="⬅️ Back", callback_data="menu:main"),
            ],
        ]
    )


def get_subs_inline_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Add sub", callback_data="subs:add"),
                InlineKeyboardButton(text="📋 List subs", callback_data="subs:list"),
            ],
            [
                InlineKeyboardButton(text="⬅️ Back", callback_data="menu:main"),
            ],
        ]
    )


def get_cabinet_inline_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📧 Mail", callback_data="cabinet:mail"),
                InlineKeyboardButton(text="⬅️ Back", callback_data="menu:main"),
            ],
        ]
    )


