from aiogram.fsm.state import StatesGroup, State


#STATES------------------------------------------------------------------------------------
class AppState(StatesGroup):
    main = State()

    movies_menu = State()
    notes_menu = State()
    subs_menu = State()
    cabinet_menu = State()

    add_movie_title = State()
    add_movie_type = State()
    add_movie_comment = State()
    delete_movie_number = State()

    add_note_title = State()
    add_note_date = State()
    delete_note_number = State()

    add_subscription_title = State()
    add_subscription_price = State()
    add_subscription_end_date = State()
    add_subscription_comment = State()
    delete_subscription_number = State()

    extend_subscription_number = State()
    extend_subscription_period = State()
    extend_custom_months = State()

    mail_list = State()
    add_mail = State()
    delete_mail = State()
    delete_service = State()

    service_list = State()
    add_service_name = State()
    add_service_login = State()
    add_service_comment = State()

