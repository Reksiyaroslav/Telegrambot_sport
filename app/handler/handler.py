from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from app.keyboard import keyboard_inlien as kb
import app.func.func as fun
from app.text import (
    text_hello,
    text_group,
    text_help,
)

router = Router()
count = 0
text = ""


# Самое первое сообщение которые видет пользователь выбирает тип
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text_hello, reply_markup=kb.keyboard_main)


@router.message(Command("help"))
async def help_start(message: Message):
    await message.answer(text_help)


@router.callback_query(F.data == "info_group")
async def info_group(callback: CallbackQuery):
    await callback.message.edit_text("Привет")
    await callback.message.answer(text_group, reply_markup=kb.keyboard_status)


@router.callback_query(F.data == "lose")
async def info_group(callback: CallbackQuery):
    await callback.message.edit_text("Lose")
    await fun.plaers_list("Barselona")
    text_list: list[str] = await fun.create_message("Barselona", "players")
    text_full = "\n".join(item for item in text_list)
    await callback.message.answer(text=text_full)


@router.callback_query(F.data == "winer")
async def info_group(callback: CallbackQuery):
    await callback.message.edit_text("Lose")
    await fun.schedule("Barselona")
    text_list: list[str] = await fun.create_message("Barselona", "schedule")
    text_full = "\n".join(item for item in text_list)
    await callback.message.answer(text=text_full)


@router.callback_query(F.data == "loream")
async def info_group(callback: CallbackQuery):
    await callback.message.edit_text("Loream")
    text = await fun.parsing_loream()
    await callback.message.answer(text=text)


# @router.message()
# async def message_stop():
