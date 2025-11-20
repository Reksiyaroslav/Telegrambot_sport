import aiohttp
import datetime
import os
from  bs4 import BeautifulSoup,Tag,ResultSet
from app.config import create_json,update_json,key_in_dict,theer_day_fille,remove_date,read_json
from app.list import list_club_list
src = ""
list_type = []
# Чтобы не думали что бот а человек зашёл к ним
heanders = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"}
def clear_list():
    # отчиска листов от  данных
    list_type.clear()
#Получения линков чтобы не плодить их 
async def parsing_html(url,type_operation,name_clan:str=None)->str:
    async with aiohttp.ClientSession() as session:
            reponse = await session.get(url=url,headers=heanders) #получения  ответа от сайта 
            reponse_text = await reponse.text() # преобразование в текст 
            if type_operation =="loream":#проверка на тип операций 
                with open(f"html/index_{type_operation}.html","w")as file :#сохранения в файл
                    file.write(reponse_text) #запись в файл
            else :
                with open(f"html/index_{type_operation}_{name_clan.lower()}.html","w")as file :
                    file.write(reponse_text)
            return reponse_text # возрашения текста страницы

async def load_html(name_clan:str,type_operaion:str):
    if type_operaion =="loream":# провека на тип данных
            with open(f"html/index_{type_operaion}.html")as file :# окрытие файла на чтения 
                text_html = file.read()# получения данных об странице с даннами из файла 
    else:
        with open(f"html/index_{type_operaion}_{name_clan}.html") as file :
            text_html = file.read()
    return text_html
#Получения данных об Loream пассхалка
async def parsing_loream ()->str:
    url = "https://en.wikipedia.org/wiki/Lorem_ipsum"#url википедей 
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
async def create_dict(list_type:list,type_operation:str):
    return {type_operation:list_type} # преобразование листа в список 
    
async def load_data(dict_types:ResultSet[Tag],type_operaion:str,type_players_or_name_clob_or=None):
        match type_operaion: # определение типа операций 
            case "players":
                for item in dict_types:
                        number_plaer =  int(item.find("td",class_="col-1 col-first left-align").text) #номер игрока 
                        img_teg = item.find("td",class_= "col-2 left-align").find("img") # получени тега фота
                        nasion_player =  img_teg.get("alt")if img_teg and img_teg.get("alt")  else "Not nassion plaerse" # получения национальности игрока 
                        name_player = item.find("td",class_= "col-2 left-align").find("a").text # имя игрока 
                        age_text:str = item.find("td",class_="col-3 center-align").text.strip() # нахождения возраста игрока 
                        age_player = int(age_text) if age_text.isdigit() else "Not age plaerse" # провека на есть возраст преобразование его в число противном случие его нет 
                        type_player =  item.find("td",class_="col-4 left-align col-position").text # получени типа игрока
                        dict_players = {
                            name_player:
                            {
                            "Nasion": nasion_player,
                            "Number": number_plaer,
                            "Age":age_player,
                            "Type plaer": type_player,
                            "Status": type_players_or_name_clob_or
                            }
                        }# запись в словарь
                        list_type.append(dict_players)# запись в списко уже готового игрока 
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
                        })# 
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
            case "static_matchs":
                dict_match = {}
                for tr in dict_types:
                    td_type_big = tr.find("td",class_="_big").text
                    if (td_type_big in ("Сыгранные матчи","% владения мячом","Точность ударов"
                                        ,"Реализация ударов (соперник)"
                                        ,"Реализация ударов","Точность ударов (соперник)","Точность ударов")):
                        td_start = tr.find("td",class_="_center _group-start _group-end").text
                        dict_match.update({td_type_big:f"Обращая {td_start}"})
                    else:
                        td_start = tr.find("td",class_="_center _group-start").text
                        td_end = tr.find("td",class_="_center _group-end").text
                        dict_match.update({td_type_big:f"{td_start}, средняя {td_end}"})
                list_type.append(dict_match)
            case "lose_winer":
                pass               
async def parsing_type_operaion(name_club:str,type_operaion:str):
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
        case "static_matchs":
            match name_club:
                case "barselona":
                    number_team = 272276
                case "real_madrid":
                    number_team =272274
                case "bavariya":
                    number_team =272294
            url = f"https://www.championat.com/football/_ucl/tournament/6560/teams/{number_team}/tstat/"
        case "loream":
            url = "https://loremipsum.io/ru/" 
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
            if(len(parameter)>0): #проверка на то что p второй вхождения 
                second_p = parameter[0] # получения 2 p
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
            case "static_matchs":
                list_tbody =  soup_Text.find_all("tbody")
                tbody_info = list_tbody[0]
                tr_list = tbody_info.find_all("tr")
                await load_data(tr_list,type_operaion=type_operaion) 
    print(list_type)
    if not os.path.exists(f"data/{name_club}.json"):
        dict_type = await create_dict(list_type,type_operaion)
        create_json(dict_type,name_club)
    if type_operaion=="loream":
        dict_type = await create_dict(list_type,type_operaion)
        name_club= type_operaion
        create_json(dict_type,name_club)
    else :  
        await remove_date(data=read_json(name_club),type_operation=type_operaion)
        update_json(list_type,name_club=name_club,type_operation=type_operaion)
    clear_list()

