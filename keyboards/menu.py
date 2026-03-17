from aiogram import Router
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

router = Router()

#LABELS------------------------------------------------------------------------------------

LABELS = {
    "ru": {
        "main_movies": "🎬 Фильмы/сериалы",
        "main_notes": "📝 Заметки",
        "main_subs": "💳 Подписки",
        "main_cabinet": "🗂️ Кабинет",
        "lang_en": "🌐 EN",
        "lang_ru": "🌐 RU",
        "reply_movies": "Фильмы",
        "reply_notes": "Заметки",
        "reply_subs": "Подписки",
        "reply_cabinet": "Кабинет",
        "reply_add_movie": "Добавить фильм/сериал",
        "reply_list_movies": "Список фильмов/сериалов",
        "reply_add_note": "Добавить заметку",
        "reply_list_notes": "Список заметок",
        "reply_add_sub": "Добавить подписку",
        "reply_list_subs": "Список подписок",
        "reply_back": "Назад",
        "reply_mail": "Почта",
        "add_movie": "➕ Добавить фильм/сериал",
        "list_movies": "📋 Список фильмов/сериал",
        "add_note": "➕ Добавить заметку",
        "list_notes": "📋 Список заметок",
        "add_sub": "➕ Добавить подписку",
        "list_subs": "📋 Список подписок",
        "mail": "📧 Почта",
        "back": "⬅️ Назад",
        "delete": "🗑️ Удалить",
        "cancel": "✖️ Отмена",
        "cancel_delete": "✖️ Отмена удаления",
        "extend": "⏫ Продлить",
        "skip": "⏭️ Пропустить",
        "add_mail": "➕ Добавить почту",
        "delete_mail": "🗑️ Удалить почту",
        "add_service": "➕ Добавить сервис",
        "delete_service": "🗑️ Удалить сервис",
        "delete_item": "Удалить {name}",
        "one_month": "1 мес",
        "three_months": "3 мес",
        "six_months": "6 мес",
        "other": "Другое",
    },
    "en": {
        "main_movies": "🎬 Movies",
        "main_notes": "📝 Notes",
        "main_subs": "💳 Subs",
        "main_cabinet": "🗂️ Cabinet",
        "lang_en": "🌐 EN",
        "lang_ru": "🌐 RU",
        "reply_movies": "Movies",
        "reply_notes": "Notes",
        "reply_subs": "Subs",
        "reply_cabinet": "Cabinet",
        "reply_add_movie": "Add movie",
        "reply_list_movies": "List movies",
        "reply_add_note": "Add note",
        "reply_list_notes": "List notes",
        "reply_add_sub": "Add sub",
        "reply_list_subs": "List subs",
        "reply_back": "Back",
        "reply_mail": "Mail",
        "add_movie": "➕ Add movie",
        "list_movies": "📋 List movies",
        "add_note": "➕ Add note",
        "list_notes": "📋 List notes",
        "add_sub": "➕ Add sub",
        "list_subs": "📋 List subs",
        "mail": "📧 Mail",
        "back": "⬅️ Back",
        "delete": "🗑️ Delete",
        "cancel": "✖️ Cancel",
        "cancel_delete": "✖️ Cancel delete",
        "extend": "⏫ Extend",
        "skip": "⏭️ Skip",
        "add_mail": "➕ Add mail",
        "delete_mail": "🗑️ Delete mail",
        "add_service": "➕ Add service",
        "delete_service": "🗑️ Delete service",
        "delete_item": "Delete {name}",
        "one_month": "1 month",
        "three_months": "3 months",
        "six_months": "6 months",
        "other": "Other",
    },
}


def normalize_lang(lang):
    return lang if lang in LABELS else "ru"


def get_label(lang, key, **kwargs):
    lang = normalize_lang(lang)
    text = LABELS[lang][key]
    return text.format(**kwargs) if kwargs else text


#REPLY MENUS-------------------------------------------------------------------------------

def get_main_reply_menu(lang="ru"):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_label(lang, "reply_movies")),
                KeyboardButton(text=get_label(lang, "reply_notes")),
            ],
            [
                KeyboardButton(text=get_label(lang, "reply_subs")),
                KeyboardButton(text=get_label(lang, "reply_cabinet")),
            ],
        ],
        resize_keyboard=True
    )
    return keyboard


def get_main_reply_movies(lang="ru"):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_label(lang, "reply_add_movie")),
                KeyboardButton(text=get_label(lang, "reply_list_movies")),
            ],
            [KeyboardButton(text=get_label(lang, "reply_back"))],
        ],
        resize_keyboard=True
    )
    return keyboard


def get_main_reply_notes(lang="ru"):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_label(lang, "reply_add_note")),
                KeyboardButton(text=get_label(lang, "reply_list_notes")),
            ],
            [KeyboardButton(text=get_label(lang, "reply_back"))],
        ],
        resize_keyboard=True
    )
    return keyboard


def get_main_reply_subs(lang="ru"):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_label(lang, "reply_add_sub")),
                KeyboardButton(text=get_label(lang, "reply_list_subs")),
            ],
            [KeyboardButton(text=get_label(lang, "reply_back"))],
        ],
        resize_keyboard=True
    )
    return keyboard


def get_main_reply_cabinet(lang="ru"):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_label(lang, "reply_mail")),
                KeyboardButton(text=get_label(lang, "reply_back")),
            ],
        ],
        resize_keyboard=True
    )
    return keyboard


def get_main_reply_mail(lang="ru"):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_label(lang, "reply_mail")),
                KeyboardButton(text=get_label(lang, "reply_back")),
            ],
        ],
        resize_keyboard=True
    )
    return keyboard


#INLINE MENUS-------------------------------------------------------------------------------

def get_main_inline_menu(lang="ru"):
    lang = normalize_lang(lang)
    lang_toggle = "lang:en" if lang == "ru" else "lang:ru"
    lang_label = get_label(lang, "lang_en") if lang == "ru" else get_label(lang, "lang_ru")
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=get_label(lang, "main_movies"), callback_data="menu:movies"),
                InlineKeyboardButton(text=get_label(lang, "main_notes"), callback_data="menu:notes"),
            ],
            [
                InlineKeyboardButton(text=get_label(lang, "main_subs"), callback_data="menu:subs"),
                InlineKeyboardButton(text=get_label(lang, "main_cabinet"), callback_data="menu:cabinet"),
            ],
            [
                InlineKeyboardButton(text=lang_label, callback_data=lang_toggle),
            ],
        ]
    )


def get_movies_inline_menu(lang="ru"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=get_label(lang, "add_movie"), callback_data="movies:add"),
                InlineKeyboardButton(text=get_label(lang, "list_movies"), callback_data="movies:list"),
            ],
            [
                InlineKeyboardButton(text=get_label(lang, "back"), callback_data="menu:main"),
            ],
        ]
    )


def get_notes_inline_menu(lang="ru"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=get_label(lang, "add_note"), callback_data="notes:add"),
                InlineKeyboardButton(text=get_label(lang, "list_notes"), callback_data="notes:list"),
            ],
            [
                InlineKeyboardButton(text=get_label(lang, "back"), callback_data="menu:main"),
            ],
        ]
    )


def get_subs_inline_menu(lang="ru"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=get_label(lang, "add_sub"), callback_data="subs:add"),
                InlineKeyboardButton(text=get_label(lang, "list_subs"), callback_data="subs:list"),
            ],
            [
                InlineKeyboardButton(text=get_label(lang, "back"), callback_data="menu:main"),
            ],
        ]
    )


def get_cabinet_inline_menu(lang="ru"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=get_label(lang, "mail"), callback_data="cabinet:mail"),
                InlineKeyboardButton(text=get_label(lang, "back"), callback_data="menu:main"),
            ],
        ]
    )
