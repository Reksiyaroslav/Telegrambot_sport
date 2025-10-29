from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
import asyncio
from app.handler.handler import router


async def main():
    load_dotenv()
    TOKE_BOT = os.getenv("TOKEN")
    bot = Bot(token=TOKE_BOT)
    dis = Dispatcher()
    dis.include_router(router)
    await dis.start_polling(bot)


if __name__ == "__main__":
    try:
        print("One bot")
        asyncio.run(main=main())
    except KeyboardInterrupt:
        print("Exit")
    except TimeoutError:
        print("Off bot")
    except RuntimeError:
        print("Off bot")
