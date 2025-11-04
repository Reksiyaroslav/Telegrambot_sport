from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from app.keyboard import keyboard_inlien as kb
import app.func.func as fun
from app.text import (
    text_hello, 
    text_group,
    text_help,
    text_club_varibal,
    text_club_var)
from app.list import list_club_list

router = Router()
count = 0
text = ""


class FConte:
    type_club: str = ""


# Самое первое сообщение которые видет пользователь выбирает тип
@router.message(CommandStart())
async def start_message(message: Message):
    await message.answer(text_hello, reply_markup=kb.keyboard_main)


@router.message(Command("help"))
async def help_start(message: Message):
    await message.answer(text_help)


@router.callback_query(F.data == "clubs")
async def info_clubs(callback: CallbackQuery):
    await callback.answer(text=text_club_varibal + callback.data)
    await callback.message.answer("Выбирай клуб который вам нужен")
    await callback.message.answer(text_club_var, reply_markup=kb.keyboard_clubs)


@router.callback_query(F.data.in_(["bavariya", "real_madrid", "barselona"]))
async def varabal_club(callback: CallbackQuery):
    FConte.type_club = callback.data
    await callback.answer(text=text_club_varibal + FConte.type_club)
    await callback.message.answer("Теперь что хотите найти")
    await callback.message.answer(text_group, reply_markup=kb.keyboard_status)


@router.callback_query(F.data.in_(["players", "coauth", "schedule"]))
async def info_type(callback: CallbackQuery):
    await callback.message.edit_text(f"Coauth: {FConte.type_club}")
    text_full = await fun.create_message(FConte.type_club, callback.data)
    await callback.message.answer(text=text_full)


@router.callback_query(F.data == "winer")
async def info_group(callback: CallbackQuery):
    await callback.message.edit_text("Pass")
    await callback.message.answer(text="пока не сделал")


@router.callback_query(F.data == "loream")
async def info_group(callback: CallbackQuery):
    await callback.message.edit_text("Loream")
    text = await fun.create_message(callback.data)
    await callback.message.answer(text=text)


@router.message(F.text)
async def handler_soup(message: Message):
    clubs = list_club_list
    new_message = message.text.lower()
    if new_message in clubs:
        FConte.type_club = message.text
        await message.answer(f"Вы выбрали: <b>{message.text}</b>")
    if (
        new_message == "schedule"
        or new_message == "players"
        or new_message == "coauth"
        and FConte.type_club != ""
    ):
        message.answer(f"Вы выбрали: <b>{message.text}</b>")
        text_full = await fun.create_message(FConte.type_club, message.text)
        await message.answer(text=text_full)
    if new_message == "loream":
        text = await fun.create_message(FConte.type_club, message.text)
        await message.answer(text)
    else:
        await message.answer("Нет такой команды")
