from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import os
import asyncio
from app.handler.handler import router
from app.list import list_club_list,list_key_list
from app.func.parsing import parsing_type_operaion
from app.config import theer_day_fille,key_in_dict,delete_file
from tkinter import Tk,Label
from PIL import ImageTk,Image
import threading
def gui_window():
    root = Tk()
    root.geometry("450x450")
    root.title("Фото подлючение бота")
    image_path = "telegram_bot.jpg"
    image_pil = Image.open(image_path)
    image_pil_rezise = image_pil.resize((450,450),Image.LANCZOS)
    image_tk = ImageTk.PhotoImage(image_pil_rezise)
    
    label = Label(root,image=image_tk)
    label.image = image_tk
    label.pack()
    # Запустите главный цикл Tkinter
    root.mainloop()
async def passing_fille():
    for club in list_club_list:
        fille_name =f"data/{club}.json"
        is_file_fife_day= await theer_day_fille(fille_name)
        is_not_key_dict = not await key_in_dict(club)
        shoul_parsding = is_not_key_dict or is_file_fife_day or not os.path.exists(fille_name)
        if shoul_parsding:
            print(f"Пасинг дл команды {club}")
            for operation in list_key_list:
                if os.path.exists(f"html/index_{club}_{operation}.html"):
                    await delete_file(club,operation)
                print(f"Выполннеи пасига дл {club} {operation}")
                await parsing_type_operaion(club,operation)
        
async def main():
    load_dotenv()
    TOKE_BOT = os.getenv("TOKEN")
    bot = Bot(token=TOKE_BOT,
                    default=DefaultBotProperties(parse_mode="HTML")
    )
    dis = Dispatcher()
    dis.include_router(router)
    gui_thread = threading.Thread(target=gui_window, daemon=True)
    gui_thread.start()

    await passing_fille()
    await dis.start_polling(bot)
    
   
   
if __name__ == "__main__":
    try:
        print("One bot")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
    except TimeoutError:
        print("Off bot")
    except RuntimeError:
        print("Off bot")
