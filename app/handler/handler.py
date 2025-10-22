from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from aiogram.filters import CommandStart, Command
import app.keyboard as kb 
import app.func.func as fun 
from  app.text import text_hello
router = Router()
@router.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer(text_hello,reply_markup=kb.keyboard_main)
