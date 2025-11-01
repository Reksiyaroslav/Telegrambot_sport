import aiohttp
from  bs4 import BeautifulSoup,Tag,ResultSet
import os
import json
list_players = []
list_data =[]
src = ""
import datetime
# Чтобы не думали что бот а человек зашёл к ним
heanders = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0"}
#Получения линков чтобы не плодить их 
async def get_url(number):
    match number:
        case 1:
            return "https://en.wikipedia.org/wiki/Lorem_ipsum"
        case 2:
            return"https://fbref.com/en/squads/206d90db/2024-2025/Barcelona-Stats"
async def parsing(url,name_clan:str,type_operation)->str:
    async with aiohttp.ClientSession() as session:
            reponse = await session.get(url=url,headers=heanders) #получения  ответа от сайта 
            reponse_text = await reponse.text()
            with open(f"html/index_{type_operation}_{name_clan.lower()}.html","w")as file :
                file.write(reponse_text)
            return reponse_text
async def full_text(list_text:list):
    return "\n".join(text for text in list_text)
async def create_json(list_type:list,name_clan:str,type_operation):
    with open(f"data/{type_operation}_{name_clan.lower()}.json","w") as fille:
        json.dump(list_type,fille,indent=3,ensure_ascii=False)
    return f"Create json {type_operation}"
async def load_html(name_clan:str,type_operaion:str):
    with open(f"html/index_{type_operaion}_{name_clan.lower()}.html") as file :
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
        return text#  вывод результата 
async def load_data_players(dict_types:ResultSet[Tag],type_players_or_name_clob_or=None):
        for item in dict_types:
                number_plaer =  int(item.find("td",class_="col-1 col-first left-align").text)
                img_teg = item.find("td",class_= "col-2 left-align").find("img") 
                nasion_player =  img_teg.get("alt")if img_teg and img_teg.get("alt")  else "Not nassion plaerse"
                name_player = item.find("td",class_= "col-2 left-align").find("a").text 
                age_text:str = item.find("td",class_="col-3 center-align").text.strip()
                age_player = int(age_text) if age_text.isdigit() else "Not age plaerse"
                type_player =  item.find("td",class_="col-4 left-align col-position").text 
                list_players.append(
                {
                    "Name" :name_player,
                    "Nasion": nasion_player,
                    "Number": number_plaer,
                    "Age":age_player,
                    "Type plaer": type_player,
                    "Status": type_players_or_name_clob_or
                })
async def load_data_schedule(dict_types:ResultSet[Tag],type_players_or_name_clob_or=None):
        if type_players_or_name_clob_or.lower() =="barselona":
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
                list_data.append(
                {
                    "Time_match" :math_time,
                    "Team_Team1": team_team1,
                    "Team_Team2": team_team2,
                    "Match_Cat":match_cat,
                })
        elif type_players_or_name_clob_or.lower() == "real madrit" or type_players_or_name_clob_or.lower() == "bavariya":
            for  item in dict_types:
                match_tag_date = item.find("div",class_="team-match__item-date")
                match_date =  match_tag_date.text.strip().replace("\n","") if match_tag_date else datetime.datetime.now().date()
                match_tag_time =  item.find("div",class_= "d-none d-sm-block")
                match_time = match_tag_time.text.strip().replace("\n","") if match_tag_time else datetime.datetime.now().time()
                match_contener = item.find("div",class_="team-match__item-name__container")
                team_match__item_team1 = match_contener.find("div",class_="team-match__item-team1").text.strip().replace("\n","")
                team_match__item_team2 = match_contener.find("div",class_="team-match__item-team2").text.strip().replace("\n","")
                team_match__item_turnir = item.find("div",class_="team-match__item-turnir d-none d-sm-block").text.strip().replace("\n","")
                list_data.append(
                {
                    "Time_match" :f"{match_date} {match_time}",
                    "Team_Team1": team_match__item_team1,
                    "Team_Team2": team_match__item_team2,
                    "Match_Cat":team_match__item_turnir,
                })                
async def plaers_list(name_clan:str)->str:
    match name_clan.lower():
        case "barselona":
            url = "https://www.soccer.ru/barselona?tournament=1380758"
        case "real madrit":
            url ="https://www.soccer.ru/real"
        case "bavariya":
            url = "https://www.soccer.ru/bavariya?tournament=1380758"
    if not os.path.exists(f"html/index_players_{name_clan.lower()}.html"):
        src = await parsing(url,name_clan,"players")
    else:
            src = await load_html(name_clan,"players")
    if not os.path.exists(f"data/data/players_{name_clan.lower()}.json"):
        soup_Text = BeautifulSoup(src,"lxml")
        tbody_list = soup_Text.find_all("tbody")
        if(len(tbody_list) > 7):
            tbody = tbody_list[7]
            plaers_list_used = tbody.find_all("tr",class_="even")
            plaers_list_not_used = tbody.find_all("tr",class_="not-played odd")
            await load_data_players(plaers_list_used,"Played")
            await load_data_players(plaers_list_not_used,"Reves")
            print(list_players)
        await create_json(list_players,name_clan,"players")
    return "God data"
async def schedule(name_clan:str):
    match name_clan.lower():
        case "barselona":
            url = "https://fc-barcelona.ru/schedule/"
        case "real madrit":
            url ="https://www.euro-football.ru/team/real_madrid/match_comming"
        case "bavariya":
            url = "https://www.euro-football.ru/team/bavariya/match_comming"
    if not os.path.exists(f"html/index_schedule_{name_clan}.html"):
        src = await parsing(url,name_clan,"schedule")
    else:
        src = await load_html(name_clan,"schedule")
    soup_Text = BeautifulSoup(src,"lxml")
    
    if  name_clan.lower() == "barselona":     
        div_matches= soup_Text.find_all("div",class_ ='matches-list-match')
        await load_data_schedule(div_matches,name_clan)
    elif name_clan.lower()=="real madrit" or name_clan.lower()=="bavariya":
            div_team_match_list = soup_Text.find("div",class_= "team-match-list team-match-list_turnir")
            div_team_match__item = div_team_match_list.find_all("div",class_="team-match__item")
            await load_data_schedule(div_team_match__item,name_clan)
    print(list_data)
    await create_json(list_data,name_clan,"schedule")
   
    return "God data "
#Создание листа с ответами для пользователя 
async def create_message(name_clan:str,type_operation:str):
    text_list = [] # Создание листа для текста
    match type_operation: # проверка на операций
        case "players": # проверка  если операция с игроками
            with open(f"data/{type_operation}_{name_clan.lower()}.json","r") as fille:# ишем нужный json с игроками
                data = json.load(fille)
            print(data)
        case "schedule":   # проверка  если операция с мачеми
            with open(f"data/{type_operation}_{name_clan.lower()}.json","r") as fille:# ишем нужный json с мачеми коретной команде
                data = json.load(fille)
            print(data)
    for item in data:
                match type_operation:# проверка на операций
                    case "players": # проверка  если операция с игроками
                        text = f"<b>Игрок</b>:\n<b>Имя:</b> {item['Name']} \n<b>Национальность:</b> {item['Nasion']}\n<b>Номер:</b> {item['Number']}"#ответ с игроками 
                    case "schedule":# проверка  если операция с мачеми
                        text = f"<b>Мачь:</b> \n<b>Дата и время:</b> {item['Time_match']} \n<b>Перва команда:</b> {item['Team_Team1']} \n<b>Вторая команда:</b> {item['Team_Team2']} \n<b>Тип мача:</b> {item['Match_Cat']}"#ответ с мачеми 
                text_list.append(text)# добовление в список
    list_players.clear()
    list_data.clear()
    return text_list# получения списка результатов для пользователя
async def coauth()->list[str]:
    pass
async def lose_wine_list()->list[str]:
    pass

