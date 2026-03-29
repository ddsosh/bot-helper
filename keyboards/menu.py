from aiogram import Router
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

router = Router()

# LABELS -----------------------------------------------------------------------------------

LABELS = {
    "ru": {
        "main_movies": "\U0001F3AC \u0424\u0438\u043b\u044C\u043C\u044B/\u0441\u0435\u0440\u0438\u0430\u043B\u044B",
        "main_notes": "\U0001F4DD \u0417\u0430\u043C\u0435\u0442\u043A\u0438",
        "main_subs": "\U0001F4B3 \u041F\u043E\u0434\u043F\u0438\u0441\u043A\u0438",
        "main_cabinet": "\U0001F5C2\uFE0F \u041A\u0430\u0431\u0438\u043D\u0435\u0442",
        "lang_en": "\U0001F310 EN",
        "lang_ru": "\U0001F310 RU",
        "reply_movies": "\u0424\u0438\u043B\u044C\u043C\u044B",
        "reply_notes": "\u0417\u0430\u043C\u0435\u0442\u043A\u0438",
        "reply_subs": "\u041F\u043E\u0434\u043F\u0438\u0441\u043A\u0438",
        "reply_cabinet": "\u041A\u0430\u0431\u0438\u043D\u0435\u0442",
        "reply_add_movie": "\u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u0444\u0438\u043B\u044C\u043C/\u0441\u0435\u0440\u0438\u0430\u043B",
        "reply_list_movies": "\u0421\u043F\u0438\u0441\u043E\u043A \u0444\u0438\u043B\u044C\u043C\u043E\u0432/\u0441\u0435\u0440\u0438\u0430\u043B\u043E\u0432",
        "reply_add_note": "\u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u0437\u0430\u043C\u0435\u0442\u043A\u0443",
        "reply_list_notes": "\u0421\u043F\u0438\u0441\u043E\u043A \u0437\u0430\u043C\u0435\u0442\u043E\u043A",
        "reply_add_sub": "\u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u043F\u043E\u0434\u043F\u0438\u0441\u043A\u0443",
        "reply_list_subs": "\u0421\u043F\u0438\u0441\u043E\u043A \u043F\u043E\u0434\u043F\u0438\u0441\u043E\u043A",
        "reply_back": "\u041D\u0430\u0437\u0430\u0434",
        "reply_mail": "\u041F\u043E\u0447\u0442\u0430",
        "add_movie": "\u2795 \u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u0444\u0438\u043B\u044C\u043C/\u0441\u0435\u0440\u0438\u0430\u043B",
        "list_movies": "\U0001F4CB \u0421\u043F\u0438\u0441\u043E\u043A \u0444\u0438\u043B\u044C\u043C\u043E\u0432/\u0441\u0435\u0440\u0438\u0430\u043B",
        "add_note": "\u2795 \u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u0437\u0430\u043C\u0435\u0442\u043A\u0443",
        "list_notes": "\U0001F4CB \u0421\u043F\u0438\u0441\u043E\u043A \u0437\u0430\u043C\u0435\u0442\u043E\u043A",
        "add_sub": "\u2795 \u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u043F\u043E\u0434\u043F\u0438\u0441\u043A\u0443",
        "list_subs": "\U0001F4CB \u0421\u043F\u0438\u0441\u043E\u043A \u043F\u043E\u0434\u043F\u0438\u0441\u043E\u043A",
        "mail": "\U0001F4E7 \u041F\u043E\u0447\u0442\u0430",
        "back": "\u2B05\uFE0F \u041D\u0430\u0437\u0430\u0434",
        "delete": "\U0001F5D1\uFE0F \u0423\u0434\u0430\u043B\u0438\u0442\u044C",
        "cancel": "\u2716\uFE0F \u041E\u0442\u043C\u0435\u043D\u0430",
        "cancel_delete": "\u2716\uFE0F \u041E\u0442\u043C\u0435\u043D\u0430 \u0443\u0434\u0430\u043B\u0435\u043D\u0438\u044F",
        "extend": "\u23EB \u041F\u0440\u043E\u0434\u043B\u0438\u0442\u044C",
        "skip": "\u23ED\uFE0F \u041F\u0440\u043E\u043F\u0443\u0441\u0442\u0438\u0442\u044C",
        "add_mail": "\u2795 \u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u043F\u043E\u0447\u0442\u0443",
        "delete_mail": "\U0001F5D1\uFE0F \u0423\u0434\u0430\u043B\u0438\u0442\u044C \u043F\u043E\u0447\u0442\u0443",
        "add_service": "\u2795 \u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u0441\u0435\u0440\u0432\u0438\u0441",
        "delete_service": "\U0001F5D1\uFE0F \u0423\u0434\u0430\u043B\u0438\u0442\u044C \u0441\u0435\u0440\u0432\u0438\u0441",
        "delete_item": "\u0423\u0434\u0430\u043B\u0438\u0442\u044C {name}",
        "one_month": "1 \u043C\u0435\u0441",
        "three_months": "3 \u043C\u0435\u0441",
        "six_months": "6 \u043C\u0435\u0441",
        "other": "\u0414\u0440\u0443\u0433\u043E\u0435",
        "choose_section": "\u0412\u044B\u0431\u0435\u0440\u0438\u0442\u0435 \u0440\u0430\u0437\u0434\u0435\u043B",
        "movies_section": "\u0420\u0430\u0437\u0434\u0435\u043B \u0444\u0438\u043B\u044C\u043C\u043E\u0432",
        "notes_section": "\u0420\u0430\u0437\u0434\u0435\u043B \u0437\u0430\u043C\u0435\u0442\u043E\u043A",
        "subs_section": "\u0420\u0430\u0437\u0434\u0435\u043B \u043F\u043E\u0434\u043F\u0438\u0441\u043E\u043A",
        "cabinet_section": "\u041A\u0430\u0431\u0438\u043D\u0435\u0442",
        "enter_title": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043D\u0430\u0437\u0432\u0430\u043D\u0438\u0435",
        "enter_type": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 M \u0438\u043B\u0438 S",
        "enter_comment": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043A\u043E\u043C\u043C\u0435\u043D\u0442\u0430\u0440\u0438\u0439",
        "enter_date_or_skip": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0434\u0430\u0442\u0443 \u0438\u043B\u0438 \u043D\u0430\u0436\u043C\u0438\u0442\u0435 \u041F\u0440\u043E\u043F\u0443\u0441\u0442\u0438\u0442\u044C",
        "enter_title_first": "\u0421\u043D\u0430\u0447\u0430\u043B\u0430 \u0432\u0432\u0435\u0434\u0438\u0442\u0435 \u043D\u0430\u0437\u0432\u0430\u043D\u0438\u0435",
        "enter_number_to_delete": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043D\u043E\u043C\u0435\u0440 \u0434\u043B\u044F \u0443\u0434\u0430\u043B\u0435\u043D\u0438\u044F:",
        "enter_sub_number": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043D\u043E\u043C\u0435\u0440 \u043F\u043E\u0434\u043F\u0438\u0441\u043A\u0438",
        "enter_number": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043D\u043E\u043C\u0435\u0440",
        "choose_period": "\u0412\u044B\u0431\u0435\u0440\u0438\u0442\u0435 \u043F\u0435\u0440\u0438\u043E\u0434:",
        "enter_months_number": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043A\u043E\u043B\u0438\u0447\u0435\u0441\u0442\u0432\u043E \u043C\u0435\u0441\u044F\u0446\u0435\u0432:",
        "enter_price": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0446\u0435\u043D\u0443",
        "enter_end_date": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0434\u0430\u0442\u0443 \u043E\u043A\u043E\u043D\u0447\u0430\u043D\u0438\u044F \u0432 \u0444\u043E\u0440\u043C\u0430\u0442\u0435 YYYY-MM-DD",
        "enter_comment_or_skip": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043A\u043E\u043C\u043C\u0435\u043D\u0442\u0430\u0440\u0438\u0439 \u0438\u043B\u0438 \u043D\u0430\u0436\u043C\u0438\u0442\u0435 \u041F\u0440\u043E\u043F\u0443\u0441\u0442\u0438\u0442\u044C",
        "service_name": "\u041D\u0430\u0437\u0432\u0430\u043D\u0438\u0435 \u0441\u0435\u0440\u0432\u0438\u0441\u0430",
        "service_login": "\u041B\u043E\u0433\u0438\u043D \u0441\u0435\u0440\u0432\u0438\u0441\u0430",
        "service_comment_or_skip": "\u041A\u043E\u043C\u043C\u0435\u043D\u0442\u0430\u0440\u0438\u0439 \u043A \u0441\u0435\u0440\u0432\u0438\u0441\u0443 \u0438\u043B\u0438 \u041F\u0440\u043E\u043F\u0443\u0441\u0442\u0438\u0442\u044C",
        "mail_name": "\u0410\u0434\u0440\u0435\u0441 \u043F\u043E\u0447\u0442\u044B",
        "select_service_to_delete": "\u0412\u044B\u0431\u0435\u0440\u0438\u0442\u0435 \u0441\u0435\u0440\u0432\u0438\u0441 \u0434\u043B\u044F \u0443\u0434\u0430\u043B\u0435\u043D\u0438\u044F:",
        "select_mail_to_delete": "\u0412\u044B\u0431\u0435\u0440\u0438\u0442\u0435 \u043F\u043E\u0447\u0442\u0443 \u0434\u043B\u044F \u0443\u0434\u0430\u043B\u0435\u043D\u0438\u044F:",
        "title_empty": "\u041D\u0430\u0437\u0432\u0430\u043D\u0438\u0435 \u043D\u0435 \u043C\u043E\u0436\u0435\u0442 \u0431\u044B\u0442\u044C \u043F\u0443\u0441\u0442\u044B\u043C",
        "title_too_long": "\u041D\u0430\u0437\u0432\u0430\u043D\u0438\u0435 \u0441\u043B\u0438\u0448\u043A\u043E\u043C \u0434\u043B\u0438\u043D\u043D\u043E\u0435 (\u043C\u0430\u043A\u0441. 50)",
        "comment_too_long": "\u041A\u043E\u043C\u043C\u0435\u043D\u0442\u0430\u0440\u0438\u0439 \u0441\u043B\u0438\u0448\u043A\u043E\u043C \u0434\u043B\u0438\u043D\u043D\u044B\u0439 (\u043C\u0430\u043A\u0441. 500)",
        "date_value_too_long": "\u0417\u043D\u0430\u0447\u0435\u043D\u0438\u0435 \u0434\u0430\u0442\u044B \u0441\u043B\u0438\u0448\u043A\u043E\u043C \u0434\u043B\u0438\u043D\u043D\u043E\u0435 (\u043C\u0430\u043A\u0441. 64)",
        "type_invalid": "\u0422\u0438\u043F \u0434\u043E\u043B\u0436\u0435\u043D \u0431\u044B\u0442\u044C 'M' \u0438\u043B\u0438 'S'",
        "price_empty": "\u0426\u0435\u043D\u0430 \u043D\u0435 \u043C\u043E\u0436\u0435\u0442 \u0431\u044B\u0442\u044C \u043F\u0443\u0441\u0442\u043E\u0439",
        "invalid_price": "\u041D\u0435\u0432\u0435\u0440\u043D\u0430\u044F \u0446\u0435\u043D\u0430",
        "end_date_empty": "\u0414\u0430\u0442\u0430 \u043E\u043A\u043E\u043D\u0447\u0430\u043D\u0438\u044F \u043D\u0435 \u043C\u043E\u0436\u0435\u0442 \u0431\u044B\u0442\u044C \u043F\u0443\u0441\u0442\u043E\u0439",
        "wrong_date_format": "\u041D\u0435\u0432\u0435\u0440\u043D\u044B\u0439 \u0444\u043E\u0440\u043C\u0430\u0442 \u0434\u0430\u0442\u044B. \u0418\u0441\u043F\u043E\u043B\u044C\u0437\u0443\u0439\u0442\u0435 YYYY-MM-DD",
        "first_use_list_movies": "\u0421\u043D\u0430\u0447\u0430\u043B\u0430 \u043E\u0442\u043A\u0440\u043E\u0439\u0442\u0435 '\u0441\u043F\u0438\u0441\u043E\u043A \u0444\u0438\u043B\u044C\u043C\u043E\u0432'",
        "first_use_list_notes": "\u0421\u043D\u0430\u0447\u0430\u043B\u0430 \u043E\u0442\u043A\u0440\u043E\u0439\u0442\u0435 '\u0441\u043F\u0438\u0441\u043E\u043A \u0437\u0430\u043C\u0435\u0442\u043E\u043A'",
        "first_use_list_subs": "\u0421\u043D\u0430\u0447\u0430\u043B\u0430 \u043E\u0442\u043A\u0440\u043E\u0439\u0442\u0435 '\u0441\u043F\u0438\u0441\u043E\u043A \u043F\u043E\u0434\u043F\u0438\u0441\u043E\u043A'",
        "enter_valid_number": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043A\u043E\u0440\u0440\u0435\u043A\u0442\u043D\u044B\u0439 \u043D\u043E\u043C\u0435\u0440",
        "invalid_number": "\u041D\u0435\u0432\u0435\u0440\u043D\u044B\u0439 \u043D\u043E\u043C\u0435\u0440",
        "no_movie_with_number": "\u0424\u0438\u043B\u044C\u043C\u0430 \u0441 \u0442\u0430\u043A\u0438\u043C \u043D\u043E\u043C\u0435\u0440\u043E\u043C \u043D\u0435\u0442",
        "no_note_with_number": "\u0417\u0430\u043C\u0435\u0442\u043A\u0438 \u0441 \u0442\u0430\u043A\u0438\u043C \u043D\u043E\u043C\u0435\u0440\u043E\u043C \u043D\u0435\u0442",
        "no_sub_with_number": "\u041F\u043E\u0434\u043F\u0438\u0441\u043A\u0438 \u0441 \u0442\u0430\u043A\u0438\u043C \u043D\u043E\u043C\u0435\u0440\u043E\u043C \u043D\u0435\u0442",
        "ok": "OK",
        "user_not_found": "\u041F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u044C \u043D\u0435 \u043D\u0430\u0439\u0434\u0435\u043D. /start",
        "user_not_found_error": "\u041E\u0448\u0438\u0431\u043A\u0430: \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u044C \u043D\u0435 \u043D\u0430\u0439\u0434\u0435\u043D. /start",
        "mail_not_found": "\u041F\u043E\u0447\u0442\u0430 \u043D\u0435 \u043D\u0430\u0439\u0434\u0435\u043D\u0430. /start",
        "service_saved_without_comment": "\u0421\u0435\u0440\u0432\u0438\u0441 \u0441\u043E\u0445\u0440\u0430\u043D\u0451\u043D \u0431\u0435\u0437 \u043A\u043E\u043C\u043C\u0435\u043D\u0442\u0430\u0440\u0438\u044F",
        "subscription_not_found": "\u041F\u043E\u0434\u043F\u0438\u0441\u043A\u0430 \u043D\u0435 \u043D\u0430\u0439\u0434\u0435\u043D\u0430",
        "subscription_extended": "\u041F\u043E\u0434\u043F\u0438\u0441\u043A\u0430 \u043F\u0440\u043E\u0434\u043B\u0435\u043D\u0430",
        "error_start_again": "\u041E\u0448\u0438\u0431\u043A\u0430. \u041D\u0430\u0447\u043D\u0438\u0442\u0435 \u0437\u0430\u043D\u043E\u0432\u043E",
        "mail_list_title": "\u041F\u043E\u0447\u0442\u0430:\n",
        "no_mails_yet": "\u041F\u043E\u043A\u0430 \u043D\u0435\u0442 \u043F\u043E\u0447\u0442",
        "services_title": "\u0421\u0435\u0440\u0432\u0438\u0441\u044B:\n",
        "no_services_yet": "\u041F\u043E\u043A\u0430 \u043D\u0435\u0442 \u0441\u0435\u0440\u0432\u0438\u0441\u043E\u0432",
        "movies_list_title": "\u0421\u043F\u0438\u0441\u043E\u043A \u0444\u0438\u043B\u044C\u043C\u043E\u0432:\n\n",
        "notes_list_title": "\u0417\u0430\u043C\u0435\u0442\u043A\u0438:\n",
        "subs_list_title": "\u041F\u043E\u0434\u043F\u0438\u0441\u043A\u0438:\n",
        "no_date": "\u0411\u0435\u0437 \u0434\u0430\u0442\u044B",
        "no_comment": "\u0411\u0435\u0437 \u043A\u043E\u043C\u043C\u0435\u043D\u0442\u0430\u0440\u0438\u044F",
        "no_mails_found": "\u041F\u043E\u0447\u0442\u044B \u043D\u0435 \u043D\u0430\u0439\u0434\u0435\u043D\u044B",
        "no_services_found": "\u0421\u0435\u0440\u0432\u0438\u0441\u044B \u043D\u0435 \u043D\u0430\u0439\u0434\u0435\u043D\u044B",
        "service_deleted": "\u0421\u0435\u0440\u0432\u0438\u0441 \u0443\u0434\u0430\u043B\u0451\u043D",
        "mail_deleted": "\u041F\u043E\u0447\u0442\u0430 \u0443\u0434\u0430\u043B\u0435\u043D\u0430",
        "reminder_5_days": "\u041D\u0430\u043F\u043E\u043C\u0438\u043D\u0430\u043D\u0438\u0435: \u043F\u043E\u0434\u043F\u0438\u0441\u043A\u0430 {title} \u0437\u0430\u043A\u0430\u043D\u0447\u0438\u0432\u0430\u0435\u0442\u0441\u044F \u0447\u0435\u0440\u0435\u0437 5 \u0434\u043D\u0435\u0439.",
        "reminder_1_day": "[!] \u041F\u043E\u0434\u043F\u0438\u0441\u043A\u0430 {title} \u0437\u0430\u043A\u0430\u043D\u0447\u0438\u0432\u0430\u0435\u0442\u0441\u044F \u0437\u0430\u0432\u0442\u0440\u0430!",
    },
    "en": {
        "main_movies": "\U0001F3AC Movies",
        "main_notes": "\U0001F4DD Notes",
        "main_subs": "\U0001F4B3 Subs",
        "main_cabinet": "\U0001F5C2\uFE0F Cabinet",
        "lang_en": "\U0001F310 EN",
        "lang_ru": "\U0001F310 RU",
        "reply_movies": "Movies",
        "reply_notes": "Notes",
        "reply_subs": "Subs",
        "reply_cabinet": "Cabinet",
        "reply_add_movie": "Add movie/series",
        "reply_list_movies": "Movies/series list",
        "reply_add_note": "Add note",
        "reply_list_notes": "Notes list",
        "reply_add_sub": "Add subscription",
        "reply_list_subs": "Subscriptions list",
        "reply_back": "Back",
        "reply_mail": "Mail",
        "add_movie": "\u2795 Add movie",
        "list_movies": "\U0001F4CB List movies",
        "add_note": "\u2795 Add note",
        "list_notes": "\U0001F4CB List notes",
        "add_sub": "\u2795 Add subscription",
        "list_subs": "\U0001F4CB List subscriptions",
        "mail": "\U0001F4E7 Mail",
        "back": "\u2B05\uFE0F Back",
        "delete": "\U0001F5D1\uFE0F Delete",
        "cancel": "\u2716\uFE0F Cancel",
        "cancel_delete": "\u2716\uFE0F Cancel deletion",
        "extend": "\u23EB Extend",
        "skip": "\u23ED\uFE0F Skip",
        "add_mail": "\u2795 Add mail",
        "delete_mail": "\U0001F5D1\uFE0F Delete mail",
        "add_service": "\u2795 Add service",
        "delete_service": "\U0001F5D1\uFE0F Delete service",
        "delete_item": "Delete {name}",
        "one_month": "1 month",
        "three_months": "3 months",
        "six_months": "6 months",
        "other": "Other",
        "choose_section": "Choose section",
        "movies_section": "Movies section",
        "notes_section": "Notes section",
        "subs_section": "Subscriptions section",
        "cabinet_section": "Cabinet",
        "enter_title": "Enter title",
        "enter_type": "Enter M or S",
        "enter_comment": "Enter comment",
        "enter_date_or_skip": "Enter date or press Skip",
        "enter_title_first": "Enter title first",
        "enter_number_to_delete": "Enter number to delete:",
        "enter_sub_number": "Enter subscription number",
        "enter_number": "Enter number",
        "choose_period": "Choose period:",
        "enter_months_number": "Enter number of months:",
        "enter_price": "Enter price",
        "enter_end_date": "Enter end date in YYYY-MM-DD format",
        "enter_comment_or_skip": "Enter comment or press Skip",
        "service_name": "Service name",
        "service_login": "Service login",
        "service_comment_or_skip": "Service comment or Skip",
        "mail_name": "Mail address",
        "select_service_to_delete": "Select service to delete:",
        "select_mail_to_delete": "Select mail to delete:",
        "title_empty": "Title cannot be empty",
        "title_too_long": "Title is too long (max 50)",
        "comment_too_long": "Comment is too long (max 500)",
        "date_value_too_long": "Date value is too long (max 64)",
        "type_invalid": "Type must be 'M' or 'S'",
        "price_empty": "Price cannot be empty",
        "invalid_price": "Invalid price",
        "end_date_empty": "End date cannot be empty",
        "wrong_date_format": "Wrong date format. Use YYYY-MM-DD",
        "first_use_list_movies": "First use 'list movies'",
        "first_use_list_notes": "First use 'list notes'",
        "first_use_list_subs": "First use 'list subscriptions'",
        "enter_valid_number": "Enter a valid number",
        "invalid_number": "Invalid number",
        "no_movie_with_number": "No movie with that number",
        "no_note_with_number": "No note with that number",
        "no_sub_with_number": "No subscription with that number",
        "ok": "OK",
        "user_not_found": "User not found. /start",
        "user_not_found_error": "Error: user not found. /start",
        "mail_not_found": "Mail not found. /start",
        "service_saved_without_comment": "Service saved without comment",
        "subscription_not_found": "Subscription not found",
        "subscription_extended": "Subscription extended",
        "error_start_again": "Error. Start again",
        "mail_list_title": "Mail:\n",
        "no_mails_yet": "No mails yet",
        "services_title": "Services:\n",
        "no_services_yet": "No services yet",
        "movies_list_title": "Movies list:\n\n",
        "notes_list_title": "Notes:\n",
        "subs_list_title": "Subscriptions:\n",
        "no_date": "No date",
        "no_comment": "No comment",
        "no_mails_found": "No mails found",
        "no_services_found": "No services found",
        "service_deleted": "Service deleted",
        "mail_deleted": "Mail deleted",
        "reminder_5_days": "Reminder: {title} ends in 5 days.",
        "reminder_1_day": "[!] {title} ends tomorrow!",
    },
}


def normalize_lang(lang):
    return lang if lang in LABELS else "ru"


def get_label(lang, key, **kwargs):
    lang = normalize_lang(lang)
    text = LABELS[lang][key]
    return text.format(**kwargs) if kwargs else text


# REPLY MENUS ------------------------------------------------------------------------------

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
        resize_keyboard=True,
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
        resize_keyboard=True,
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
        resize_keyboard=True,
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
        resize_keyboard=True,
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
        resize_keyboard=True,
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
        resize_keyboard=True,
    )
    return keyboard


# INLINE MENUS -----------------------------------------------------------------------------

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
