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

class FConte:
    type_club:str = ""
# Самое первое сообщение которые видет пользователь выбирает тип
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text_hello, reply_markup=kb.keyboard_main)


@router.message(Command("help"))
async def help_start(message: Message):
    await message.answer(text_help)


@router.callback_query(F.data == "clubs")
async def info_clubs(callback: CallbackQuery):
    await callback.message.answer("Выбери клуб который вам нужен")
    await callback.message.answer(text_group, reply_markup=kb.keyboard_clubs)
@router.callback_query(F.data == "barselona")
async def barselona_club(callback: CallbackQuery):
    FConte.type_club = "Barselona"
    await callback.message.answer("Теперь что хотите найти")
    await callback.message.answer(text_group, reply_markup=kb.keyboard_status)
@router.callback_query(F.data == "bavariya")
async def varabal_club(callback: CallbackQuery):
    FConte.type_club = "Bavariya"
    await callback.message.answer("Теперь что хотите найти")
    await callback.message.answer(text_group, reply_markup=kb.keyboard_status)
@router.callback_query(F.data == "real madrit")
async def real_mandrit_club(callback: CallbackQuery):
    FConte.type_club = "Real madrit"
    await callback.message.answer("Теперь что хотите найти")
    await callback.message.answer(text_group, reply_markup=kb.keyboard_status)
@router.callback_query(F.data == "plaers_data")
async def info_players(callback: CallbackQuery):
    await callback.message.edit_text(f"Игроки: {FConte.type_club}")
    await fun.plaers_list(FConte.type_club)
    text_list: list[str] = await fun.create_message(FConte.type_club, "players")
    text_full = await fun.full_text(text_list)
    await callback.message.answer(text=text_full)
@router.callback_query(F.data == "schedule")
async def info_schedule(callback: CallbackQuery):
    await callback.message.edit_text(f"Schedule: {FConte.type_club}")
    await fun.schedule(FConte.type_club)
    text_list: list[str] = await fun.create_message(FConte.type_club, "schedule")
    text_full = await fun.full_text(text_list)
    await callback.message.answer(text=text_full)


@router.callback_query(F.data == "winer")
async def info_group(callback: CallbackQuery):
    await callback.message.edit_text("Pass")
    await callback.message.answer(text="пока не сделал")


@router.callback_query(F.data == "loream")
async def info_group(callback: CallbackQuery):
    await callback.message.edit_text("Loream")
    text = await fun.parsing_loream()
    await callback.message.answer(text=text)


@router.message(F.text)
async def message_stop(message:Message):
    clubs = ("barselona","real madrit","bavariya")
    if message.text.lower() in clubs:
        FConte.type_club = message.text
        await message.answer(f"Вы выбрали <b>{message.text}</b>")
    elif message.text == "schedule" or message.text =="players" and  FConte.type_club!="":
        message.answer(f"Вы выбрали <b>{message.text}</b>")
        if message.text == "players":
            await fun.plaers_list(FConte.type_club)
        elif message.text == 'schedule':
            await fun.schedule(FConte.type_club)
        text_list =await fun.create_message(FConte.type_club,message.text)
        text_full = await fun.full_text(text_list)
        await message.answer(text=text_full)
    elif message.text =="loream":
        text = await fun.parsing_loream
        await message.answer(text)
    else:
        await message.answer("Нет такой команды")


        
