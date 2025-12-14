from datetime import datetime
import os
import json
import time

async def key_in_dict(name_clan) -> bool:
    if os.path.exists(f"data/{name_clan}.json"):
        data = read_json(name_clan)
        key_json = ("players", "schedule", "coauth","static_matchs")
        return all(key in data for key in key_json)
    return False

def create_json(data: dict, name_clan: str):
    with open(f"data/{name_clan}.json", "w") as fille:
        json.dump(data, fille, indent=3, ensure_ascii=False)
    return "Create json"

def read_json(name_club) -> dict:
    with open(f"data/{name_club}.json", "r") as fille:
        return json.load(fille)
def dict_in_object(date_update:dict,list_unic:list):
    for element in list_unic:
        if not isinstance(element,dict) and element==date_update:
            return True
    return False


def update_json(date_update: list | str | dict, name_club: str, type_operation):
    data = read_json(name_club)
    current = data.get(type_operation)
    if not isinstance(current, list):
        current = []
    if isinstance(date_update, list):
        list_unic = list(current)
        for item in date_update:
            if not any(isinstance(exsit,dict) and item == exsit for exsit in list_unic):
                if item not in list_unic:
                    list_unic.append(item)
            else :
                if item not in list_unic:
                   list_unic.append(item) 
        data[type_operation] = list_unic
    else:
        data[type_operation] = date_update
    create_json(data, name_club)
async def remove_date(data:dict,type_operation):
    if  type_operation not in  data:
        return data
    now_datetime = datetime.now() 
    #str_datetime = datetime.strptime(now_datetime,"%d.%m.%Y %H:Y%")
    list_update = []
    for item in data[type_operation]:
        datetimedata_str =item.get("Time_match")
        if datetimedata_str:
            try:
                if ":" in datetimedata_str:
                    datedata_datetime = datetime.strptime(datetimedata_str,"%d.%m.%Y %H:%M")
                if now_datetime < datedata_datetime:
                    list_update.append(item)
            except ValueError:    
                list_update.append(item)
        else:
            list_update.append(item)
    data[type_operation] =  list_update
    return data
                
async def theer_day_fille(filename: str):
    now_time = time.time()
    theer_age_day = now_time - 3 * 24 * 60 * 60
    if os.path.exists(filename):
        time_fille_update = os.path.getmtime(filename=filename)
        return time_fille_update < theer_age_day
async def delete_file (name_club:str,type_operaiton:str):
        os.remove(f"html/index_{type_operaiton}_{name_club}.html")    