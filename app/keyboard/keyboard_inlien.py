from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.text import (
    text_keyboard_main,
    text_keyboard_group_plaers,
    text_keyboard_plaers,
    text_keyboard_coach,
    text_keyboar_lose,
    text_keyboar_winer,
    text_keyboar_schedule,
    text_message_tourney,
)

keyboard_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=text_keyboard_main, callback_data="loream")],
        [
            InlineKeyboardButton(
                text=text_keyboard_group_plaers, callback_data="info_group"
            )
        ],
    ]
)
keyboard_plaer_cohuct = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=text_keyboard_plaers, callback_data="plaers_data")],
        [InlineKeyboardButton(text=text_keyboard_coach, callback_data="coach")],
    ]
)
keyboard_status = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=text_keyboar_lose, callback_data="lose")],
        [InlineKeyboardButton(text=text_keyboar_winer, callback_data="winer")],
        [InlineKeyboardButton(text=text_message_tourney, callback_data="tourney")],
        [InlineKeyboardButton(text=text_keyboar_schedule, callback_data="schedule")],
    ]
)
