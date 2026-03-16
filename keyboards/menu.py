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
            [KeyboardButton(text="del movie"), KeyboardButton(text="back")],
        ],
        resize_keyboard=True
    )
    return keyboard


def get_main_reply_notes():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="add note"), KeyboardButton(text="list notes")],
            [KeyboardButton(text="del note"), KeyboardButton(text="back")],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_main_reply_subs():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="add sub"), KeyboardButton(text="list subs")],
            [KeyboardButton(text="del sub"), KeyboardButton(text="back")],
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
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1", url="https://telegram.org")],
            [InlineKeyboardButton(text="2", callback_data="info_more"),
             InlineKeyboardButton(text="3", callback_data="info_more")]
        ]
    )
    return keyboard


