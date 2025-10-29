import aiohttp
from  bs4 import BeautifulSoup,ResultSet,Tag
import os
import asyncio
import datetime
list_players = []
list_data = []
heanders = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0"}
src = ""
#Получения линков чтобы не плодить их 
import json
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
    if not os.path.exists(f"html/index_players_{name_clan}.html"):
        async with aiohttp.ClientSession() as session:
            reponse = await session.get(url=url,headers=heanders) #получения  ответа от сайта 
            reponse_text = await reponse.text()
            with open(f"html/index_players_{name_clan}.html","w")as file :
                file.write(reponse_text)
            src = reponse_text
    
    else:
        with open(f"html/index_players_{name_clan}.html") as file :
            src = file.read()
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
            with open(f"data/players_{name_clan.lower()}.json","w") as fille:
                json.dump(list_players,fille,indent=3,ensure_ascii=False)
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
        async with aiohttp.ClientSession() as session:
            reponse = await session.get(url=url,headers=heanders) #получения  ответа от сайта 
            reponse_text = await reponse.text()
            with open(f"html/index_schedule_{name_clan}.html","w")as file :
                file.write(reponse_text)
            src = reponse_text
    else:
        with open(f"html/index_schedule_{name_clan}.html") as file :
            src = file.read()
    soup_Text = BeautifulSoup(src,"lxml")
    match name_clan.lower():
        case "barselona":
            div_matches= soup_Text.find_all("div",class_ ='matches-list-match')
            await load_data_schedule(div_matches,name_clan)
        case "real madrit":
            div_team_match_list = soup_Text.find("div",class_= "team-match-list team-match-list_turnir")
            div_team_match__item = div_team_match_list.find_all("div",class_="team-match__item")
            await load_data_schedule(div_team_match__item,name_clan)
    print(list_data)
    with open(f"data/schedule_{name_clan.lower()}.json","w") as fille:
            json.dump(list_data,fille,indent=3,ensure_ascii=False)
    return "God data "

async def create_message(name_clan:str,type_operation:str):
    text_list = []
    match type_operation:
        case "players":
            with open(f"data/players_{name_clan.lower()}.json","r") as fille:
                data = json.load(fille)
            print(data)
        case "schedule": 
            with open(f"data/schedule_{name_clan.lower()}.json","r") as fille:
                data = json.load(fille)
            print(data)
    for item in data:
                match type_operation:
                    case "players":
                        text = f"Игрок Имя:{item['Name']} Национальность:{item['Nasion']} Номер:{item['Number']}"
                    case "schedule":
                        text = f"Мачь: Дата и время: {item['Time_match']} Перва команда: {item['Team_Team1']} Втора команда: {item['Team_Team2']} Тип мача: {item['Match_Cat']}"
                text_list.append(text)
    print(text_list)
    list_players.clear()
    list_data.clear()
    return text_list

async def main():
   await plaers_list("Barselona")
   await create_message("Barselona","players")
   await plaers_list("Real Madrit")
   await create_message("Real Madrit","players")
   await schedule("Barselona")
   await create_message("Barselona","schedule")
   await schedule("Real Madrit")
   await   create_message("Real Madrit","schedule")
if __name__ == "__main__":
        print("Зарпуск парсинга")
        asyncio.run(main=main())