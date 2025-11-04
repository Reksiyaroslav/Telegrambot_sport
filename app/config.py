import datetime
import os
import json
import time


async def key_in_dict(name_clan) -> bool:
    if os.path.exists(f"data/{name_clan}.json"):
        data = read_json(name_clan)
        key_json = ("players", "schedule", "coauth")
        return all(key in data for key in key_json)
    return False


def create_json(data: dict, name_clan: str):
    with open(f"data/{name_clan}.json", "w") as fille:
        json.dump(data, fille, indent=3, ensure_ascii=False)
    return f"Create json"


def read_json(name_club) -> dict:
    with open(f"data/{name_club}.json", "r") as fille:
        return json.load(fille)


def update_json(date_update: list | str | dict, name_club: str, type_operation):
    data = read_json(name_club)
    current = data.get(type_operation)
    if not isinstance(current, list):
        current = []
    if isinstance(date_update, list) and isinstance(date_update, list):
        list_unic = list(current)
        for item in date_update:
            if item not in list_unic:
                list_unic.append(item)
            data[type_operation] = list_unic
    else:
        data[type_operation] = date_update
    create_json(data, name_club)


async def theer_day_fille(filename: str):
    now_time = time.time()
    theer_age_day = now_time - 3 * 24 * 60 * 60
    if os.path.exists(filename):
        time_fille_update = os.path.getctime(filename=filename)
        return time_fille_update < theer_age_day
