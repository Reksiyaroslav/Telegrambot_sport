from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.text import (
    text_keyboard_main,
    text_keyboard_group_plaers,
    text_keyboard_plaers,
    text_keyboard_coach,
    text_keyboar_lose,
    text_keyboar_static_matchs,
    text_keyboar_schedule,
    text_message_tourney,
    text_barselona,
    text_bavariya,
    text_relal_madrit,
    text_clubs,
)

keyboard_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=text_keyboard_main, callback_data="loream")],
        [InlineKeyboardButton(text=text_clubs, callback_data="clubs")],
    ]
)

keyboard_status = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=text_keyboar_lose, callback_data="lose")],
        [InlineKeyboardButton(text=text_keyboar_static_matchs, callback_data="static_matchs")],
        [InlineKeyboardButton(text=text_message_tourney, callback_data="tourney")],
        [InlineKeyboardButton(text=text_keyboar_schedule, callback_data="schedule")],
        [InlineKeyboardButton(text=text_keyboard_plaers, callback_data="players")],
        [InlineKeyboardButton(text=text_keyboard_coach, callback_data="coauth")],
    ]
)
keyboard_clubs = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=text_barselona, callback_data="barselona")],
        [InlineKeyboardButton(text=text_bavariya, callback_data="bavariya")],
        [InlineKeyboardButton(text=text_relal_madrit, callback_data="real_madrid")],
    ]
)
