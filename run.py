from aiogram import Bot,Dispatcher
from dotenv import load_dotenv
import os 
import asyncio
from app.handler.handler import router
async def main():
    load_dotenv()
    TOKEn_BOT = os.getenv("TOKEN")
    bot = Bot(token=TOKEn_BOT)
    dis =  Dispatcher(bot) 
    dis.include_router(router)
    dis.start_polling()

if __name__ =="__run__":
    try:
        print("One bot")
        asyncio.run(main=main)
    except KeyboardInterrupt:
        print("Exit")
    except TimeoutError:
        print("Off bot")
