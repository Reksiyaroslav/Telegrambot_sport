import asyncio
import aiohttp
import datetime
import os
from  bs4 import BeautifulSoup,Tag,ResultSet
from app.config import create_json, read_json,update_json,key_in_dict,theer_day_fille
from app.list import list_club_list
src = ""
list_type = []
# Чтобы не думали что бот а человек зашёл к ним
heanders = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0"}
def clear_list():
    list_type.clear()
#Получения линков чтобы не плодить их 
async def parsing_html(url,type_operation,name_clan:str=None)->str:
    async with aiohttp.ClientSession() as session:
            reponse = await session.get(url=url,headers=heanders) #получения  ответа от сайта 
            reponse_text = await reponse.text()
            if type_operation =="loream":
                with open(f"html/index_{type_operation}.html","w")as file :
                    file.write(reponse_text)
            else :
                with open(f"html/index_{type_operation}_{name_clan.lower()}.html","w")as file :
                    file.write(reponse_text)
            return reponse_text

async def load_html(name_clan:str,type_operaion:str):
    if type_operaion =="loream":
            with open(f"html/index_{type_operaion}.html")as file :
                text_html = file.read()
    else:
        with open(f"html/index_{type_operaion}_{name_clan}.html") as file :
            text_html = file.read()
    return text_html
#Получения данных об Loream пассхалка
async def parsing_loream ()->str:
    url = "https://en.wikipedia.org/wiki/Lorem_ipsum"  #url википедей 
   #Создание сесий для сайта 
    async with aiohttp.ClientSession() as session:
        reponse = await session.get(url=url,headers=heanders) #получения  ответа от сайта 
        reponse_text = await reponse.text() # получения данных с кодировкой 
        soup_Text = BeautifulSoup( reponse_text,"lxml") # обрашения к странице для извлечения данных 
        containe= soup_Text.find("div",class_="mw-page-container-inner") # переход в div с классом  mw-page-container-inner
        content_container =  containe.find("div",class_="mw-content-container")# переход в div с классом  mw-content-container-inner
        main = content_container.find("main")# переход в main   
        div_bodycontext = main.find("div",id="bodyContent") # переход в div с id  bodyContent
        div_mw = div_bodycontext.find("div",class_="mw-body-content")# переход в div с классом  mw-body-content
        div_mw1 = div_mw.find("div",class_="mw-content-ltr mw-parser-output") # переход в div с классом mw-content-ltr mw-parser-output
        parameter = div_mw1.find_all("p") # поиск всех тегов p 
        if(len(parameter)>1): #проверка на то что p второй вхождения 
            second_p = parameter[1] # получения 2 p
            text = second_p.text if second_p else "fsasfasffsd" # запись в текст данных с тега p если их нет то береберда 
        dict_loream = {
            "loream":text    
        }
        create_json(dict_loream,"loream")
async def parsing_full(name_clan:str, type_operation):
    if type_operation == "loream":
        await parsing_loream()
        return
    else:
        match type_operation:
            case "players":
                await plaers_list(name_clan)
            case "schedule":
                await schedule(name_clan)
            case "coauth":
                await coauth(name_clan)
       
async def create_dict(list_type:list,type_operation:str):
    return {type_operation:list_type}
    
async def load_data(dict_types:ResultSet[Tag],type_operaion:str,type_players_or_name_clob_or=None):
        match type_operaion:
            case "players":
                for item in dict_types:
                        number_plaer =  int(item.find("td",class_="col-1 col-first left-align").text)
                        img_teg = item.find("td",class_= "col-2 left-align").find("img") 
                        nasion_player =  img_teg.get("alt")if img_teg and img_teg.get("alt")  else "Not nassion plaerse"
                        name_player = item.find("td",class_= "col-2 left-align").find("a").text 
                        age_text:str = item.find("td",class_="col-3 center-align").text.strip()
                        age_player = int(age_text) if age_text.isdigit() else "Not age plaerse"
                        type_player =  item.find("td",class_="col-4 left-align col-position").text 
                        dict_players = {
                            name_player:
                            {
                            "Nasion": nasion_player,
                            "Number": number_plaer,
                            "Age":age_player,
                            "Type plaer": type_player,
                            "Status": type_players_or_name_clob_or
                            }
                        }
                        list_type.append(dict_players)
            case "schedule":
                if type_players_or_name_clob_or == list_club_list[0]:
                    for  item in dict_types:
                        match_detail = item.find("span", class_="match-details")
                        if match_detail is None:
                            continue
                        match_time_tag = match_detail.find("span",class_="match-time")
                        time_tag =  match_time_tag.find("time")
                        math_time = time_tag.text if time_tag else datetime.datetime.now()
                        match_title = match_detail.find("span",class_="match-title")
                        team_team1  = match_title.find("span",class_="team team1").find("span").text
                        team_team2  = match_title.find("span",class_="team team2").find("span").text
                        match_cat =  item.find("span",class_="match-cat").find("span").text
                        list_type.append(
                        {
                            "Time_match" :math_time,
                            "Team_Team1": team_team1,
                            "Team_Team2": team_team2,
                            "Match_Cat":match_cat,
                        })
                elif type_players_or_name_clob_or in (list_club_list[1],list_club_list[2]):
                    for  item in dict_types:
                        match_tag_date = item.find("div",class_="team-match__item-date")
                        match_date =  match_tag_date.text.strip().replace("\n","") if match_tag_date else datetime.datetime.now().date()
                        match_tag_time =  item.find("div",class_= "d-none d-sm-block")
                        match_time = match_tag_time.text.strip().replace("\n","") if match_tag_time else datetime.datetime.now().time()
                        match_contener = item.find("div",class_="team-match__item-name__container")
                        team_match__item_team1 = match_contener.find("div",class_="team-match__item-team1").text.strip().replace("\n","")
                        team_match__item_team2 = match_contener.find("div",class_="team-match__item-team2").text.strip().replace("\n","")
                        team_match__item_turnir = item.find("div",class_="team-match__item-turnir d-none d-sm-block").text.strip().replace("\n","")
                        list_type.append(
                        {
                            "Time_match" :f"{match_date} {match_time}",
                            "Team_Team1": team_match__item_team1,
                            "Team_Team2": team_match__item_team2,
                            "Match_Cat":team_match__item_turnir,
                        })
            case "coauth":
                name_coath = type_players_or_name_clob_or
                list_operaon = []
                for tr_tag in dict_types:
                    tag_td =  tr_tag.find("td").text.strip().replace("\n","")
                    list_operaon.append(tag_td) 
                relult = []
                for item in list_operaon:
                    part = item.split(":",1)[1].strip()
                    relult.append(part)
                list_type.append({
                    "name":name_coath,
                   "Nassion": relult[0],
                    "Nire_date":relult[1],
                    "Type_club": relult[2],
                })
            case "lose_winer":
                pass               
async def parsing_type_operaion(name_club,type_operaion):
    match type_operaion: 
        case  "players":
            if name_club in ("barselona","bavariya"):
                url = f"https://www.soccer.ru/{name_club}?tournament=1380758"
            else:
                url =f"https://www.soccer.ru/real"
        case "schedule":
            if name_club=="barselona":
                url = "https://fc-barcelona.ru/schedule/"
            else :
                url =f"https://www.euro-football.ru/team/{name_club}/match_comming"
        case "coauth":
            name_coath = ""
            match name_club:
                case "barselona":
                    name_coath ="hans-diter-flik"
                case "real_madrid":
                    name_coath = "habi-alonso"
                case "bavariya":
                    name_coath = "vensan-kompani"
            url = f"https://www.soccer.ru/coaches/{name_coath}?tournament=1380758"
        case "loream":
            url = "https://en.wikipedia.org/wiki/Lorem_ipsum" 
    if not os.path.exists(f"html/index_{type_operaion}_{name_club}.html"):
        src = await parsing_html(url,name_clan=name_club,type_operation=type_operaion)
    if type_operaion == "loream":
        src =await parsing_html(url,type_operation=type_operaion)
    else:
        src = await load_html(name_club,type_operaion)
    oder_ten  = await theer_day_fille(f"data/{name_club}.json") 
    oder_key = await key_in_dict(name_club) 
    if type_operaion=="loream":
            soup_Text = BeautifulSoup(src,"lxml")
            parameter = soup_Text.find_all("p") # поиск всех тегов p 
            if(len(parameter)>1): #проверка на то что p второй вхождения 
                second_p = parameter[1] # получения 2 p
                text = second_p.text if second_p else "fsasfasffsd" # запись в текст данных с тега p если их нет то береберда 
            list_type.append(text)
    if not os.path.exists(f"data/{name_club}.json") or oder_ten or  not oder_key:
        soup_Text = BeautifulSoup(src,"lxml")
        match type_operaion:
            case "players":
                tbody_list = soup_Text.find_all("tbody") 
                if(len(tbody_list) > 7):
                    tbody = tbody_list[7]
                    plaers_list_used = tbody.find_all("tr",class_="even")
                    plaers_list_not_used = tbody.find_all("tr",class_="not-played odd")
                    await load_data(dict_types = plaers_list_used,type_operaion = type_operaion,type_players_or_name_clob_or = "Played")
                    await load_data(dict_types = plaers_list_not_used,type_operaion = type_operaion,type_players_or_name_clob_or= "Reves")
            case "schedule":
                if name_club == "barselona":     
                    div_matches= soup_Text.find_all("div",class_ ='matches-list-match')
                    await load_data(div_matches,type_operaion=type_operaion,type_players_or_name_clob_or=name_club)
                elif name_club in ("real_madrid" ,"bavariya"):
                    div_team_match_list = soup_Text.find("div",class_= "team-match-list team-match-list_turnir")
                    div_team_match__item = div_team_match_list.find_all("div",class_="team-match__item")
                    await load_data(div_team_match__item,type_operaion=type_operaion,type_players_or_name_clob_or=name_club) 
            case 'coauth':
                div_center_inner_content = soup_Text.find("div",id="center").find("div",class_="center-inner").find("div",class_="center-inner-content")
                name_tag_coath_text = ""
                if name_club == "barselone":
                    name_tag_coath_text = div_center_inner_content.find("h1",class_="site-title").text
                else :
                    name_tag_coath_text = div_center_inner_content.find("h1",class_="site-title copy-protected").text
                tbody_tag_list =  div_center_inner_content.find_all("tbody")
                tbody_iformaion = tbody_tag_list[0]
                list_tr = tbody_iformaion.find_all("tr")
                await load_data(list_tr,type_operaion=type_operaion,type_players_or_name_clob_or=name_tag_coath_text)
    if not os.path.exists(f"data/{name_club}.json"):
        dict_type = await create_dict(list_type,type_operaion)
        create_json(dict_type,name_club)
    if type_operaion=="loream":
        dict_type = await create_dict(list_type,type_operaion)
        name_club= type_operaion
        create_json(dict_type,name_club)
    else : update_json(list_type,name_club=name_club,type_operation=type_operaion)
    clear_list()
async def plaers_list(name_clan:str)->str:
    if name_clan in ("barselona","bavariya"):
        url = f"https://www.soccer.ru/{name_clan}?tournament=1380758"
    else:
        url =f"https://www.soccer.ru/real"
            
    if not os.path.exists(f"html/index_players_{name_clan}.html"):
        src = await parsing_html(url,name_clan,"players")
    else:
        src = await load_html(name_clan,"players")
    oder_ten  = await theer_day_fille(f"data/{name_clan}.json") 
    oder_key = await key_in_dict(name_clan) 
    if not os.path.exists(f"data/{name_clan}.json") or oder_ten or  not oder_key:
        soup_Text = BeautifulSoup(src,"lxml")
        tbody_list = soup_Text.find_all("tbody") 
        if(len(tbody_list) > 7):
            tbody = tbody_list[7]
            plaers_list_used = tbody.find_all("tr",class_="even")
            plaers_list_not_used = tbody.find_all("tr",class_="not-played odd")
            await load_data(dict_types = plaers_list_used,type_operaion = "players",type_players_or_name_clob_or = "Played")
            await load_data(dict_types = plaers_list_not_used,type_operaion = "players",type_players_or_name_clob_or= "Reves")
            print(list_type)
       
    if not os.path.exists(f"data/{name_clan}.json"):
        dict_players = await create_dict(list_type,"players")
        create_json(dict_players,name_clan)
    else : update_json(list_type,name_club=name_clan,type_operation="players")
    clear_list()
    return "God data"
async def schedule(name_clan:str):
    if name_clan=="barselona":
        url = "https://fc-barcelona.ru/schedule/"
    else :
        url =f"https://www.euro-football.ru/team/{name_clan}/match_comming"
    print(url)
    if not os.path.exists(f"html/index_schedule_{name_clan}.html"):
        src = await parsing_html(url,name_clan,"schedule")
    else:
        src = await load_html(name_clan,"schedule")
    soup_Text = BeautifulSoup(src,"lxml")
    
    if  name_clan.lower() == "barselona":     
        div_matches= soup_Text.find_all("div",class_ ='matches-list-match')
        await load_data(div_matches,type_operaion="schedule",type_players_or_name_clob_or=name_clan)
    elif name_clan.lower()=="real_madrid" or name_clan.lower()=="bavariya":
            div_team_match_list = soup_Text.find("div",class_= "team-match-list team-match-list_turnir")
            div_team_match__item = div_team_match_list.find_all("div",class_="team-match__item")
            await load_data(div_team_match__item,type_operaion="schedule",type_players_or_name_clob_or=name_clan)
    if not os.path.exists(f"data/{name_clan}.json"):
        dict_data = await create_dict(list_type,"schedule")
        create_json(dict_data,name_clan)
    else : update_json(list_type,name_club=name_clan,type_operation="schedule")
    clear_list()
    return "God data "
async def coauth(name_club:str)->list[str]:
    name_coath = ""
    match name_club:
        case "barselona":
            name_coath ="hans-diter-flik"
        case "real_madrid":
            name_coath = "habi-alonso"
        case "bavariya":
            name_coath = "vensan-kompani"
    url = f"https://www.soccer.ru/coaches/{name_coath}?tournament=1380758"
    if not os.path.exists(f"html/index_coauth_{name_club}.html"):
        src = await parsing_html(url,name_club,"coauth")
    else:
        src = await load_html(name_club,"coauth")
        
    soup_Text = BeautifulSoup(src,"lxml")
    div_center_inner_content = soup_Text.find("div",id="center").find("div",class_="center-inner").find("div",class_="center-inner-content")
    name_tag_coath_text = ""
    if name_club == "barselone":
        name_tag_coath_text = div_center_inner_content.find("h1",class_="site-title").text
    else :
        name_tag_coath_text = div_center_inner_content.find("h1",class_="site-title copy-protected").text
    tbody_tag_list =  div_center_inner_content.find_all("tbody")
    tbody_iformaion = tbody_tag_list[0]
    list_tr = tbody_iformaion.find_all("tr")
    await load_data(list_tr,type_operaion="coauth",type_players_or_name_clob_or=name_tag_coath_text)
    if not os.path.exists(f"data/{name_club}.json"):
        dict_coauth = await create_dict(list_type,"coauth")
        create_json(dict_coauth,name_club)
    else:  update_json(list_type,name_club,"coauth")
    clear_list()
async def lose_wine_list()->list[str]:
    pass

async def create_message(name_clan:str,type_operation:str=None)->str:
    text_list = [] # Создание листа для текста
    data =  read_json(name_clan)
    if name_clan =="loream":
        text_list.append(data["loream"])
    else:     
        print(data[f"{type_operation}"])
        for item in data[f"{type_operation}"]:
                    match type_operation:# проверка на операций
                        case "players": # проверка  если операция с игроками
                            for key in item:  
                                text = f"<b>Игрок</b>:\n<b>Имя:</b> {key} \n<b>Национальность:</b> {item[key]['Nasion']}\n<b>Номер:</b> {item[key]['Number']}"#ответ с игроками 
                        case "schedule":# проверка  если операция с мачеми
                            text = f"""<b>Мачь:</b> \n<b>Дата и время:</b> {item['Time_match']} \n<b>Перва команда:</b> {item['Team_Team1']} \n <b>Вторая команда:</b> {item['Team_Team2']} \n<b>Тип мача:</b> {item['Match_Cat']}"""#ответ с мачеми
                        case "coauth":
                            text = f"""<b>Тренер</b>:\n<b>Имя:</b> {item['name']}\n<b>Национальность: {item['Nassion']}</b>\n<b>Дата рождения и возраст: </b>{item['Nire_date']}\n<b> Тренер команды:</b> {item['Type_club']}
                        """    
                    text_list.append(text)# добовление в список
    text_full = "\n".join(text for text in text_list)
    return text_full# получения списка результатов для пользователя

async def main():
   #await plaers_list("Barselona")
   #await create_message("Barselona","players")
   #await plaers_list("Real Madrit")
   #await create_message("Real Madrit","players")
   #await coauth("barselona")
   #await create_message("barselona","coauth")
   await parsing_loream()
   print(await   create_message("loream"))
   #await schedule("Bavariya")
   #await   create_message("Bavariya","schedule")
if __name__ == "__main__":
        print("Зарпуск парсинга")
        asyncio.run(main=main())