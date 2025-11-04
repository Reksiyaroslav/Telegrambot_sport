from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import os
import asyncio
from app.handler.handler import router
from app.list import list_club_list,list_key_list
from app.func.parsing import parsing_type_operaion
from app.config import theer_day_fille,key_in_dict
async def main():
    shoul_parsding = False
    for club in list_club_list:
        fille_name =f"data/{club}.json"
        for operation in list_key_list:
            if not os.path.exists(fille_name):
                shoul_parsding =True
            else:
                is_file_fife_day= await theer_day_fille(fille_name)
                is_not_key_dict = not await key_in_dict(club)
                if is_file_fife_day or is_not_key_dict:
                    shoul_parsding =True
            if shoul_parsding:
                await parsing_type_operaion(club,operation)
            else:
                break
    load_dotenv()
    TOKE_BOT = os.getenv("TOKEN")
    bot = Bot(token=TOKE_BOT,
    default=DefaultBotProperties(parse_mode="HTML"))
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
