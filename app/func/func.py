from app.config import read_json

# Создание  ответами для пользователя
async def create_message(name_clan: str, type_operation: str = None) -> str:
    text_list = []  # Создание листа для текста
    data = read_json(name_clan)
    if name_clan == "loream":
        print(data["loream"])
        text_list.append(data["loream"][0])
    else:
        print(data[f"{type_operation}"])
        for item in data[f"{type_operation}"]:
            match type_operation:  # проверка на операций
                case "players":  # проверка  если операция с игроками
                    for key in item:
                        text = f"<b>Игрок</b>:\n<b>Имя:</b> {key} \n<b>Национальность:</b> {item[key]['Nasion']}\n<b>Номер:</b> {item[key]['Number']}"  # ответ с игроками
                case "schedule":  # проверка  если операция с мачеми
                    text = f"""<b>Матч:</b> \n<b>Дата и время:</b> {item['Time_match']} \n<b>Первая команда:</b> {item['Team_Team1']} \n<b>Вторая команда:</b> {item['Team_Team2']} \n<b>Тип мача:</b> {item['Match_Cat']}"""  # ответ с мачеми
                case "coauth":
                    text = f"""<b>Тренер</b>:\n<b>Имя:</b> {item['name']}\n<b>Национальность</b>: {item['Nassion']}\n<b>Дата рождения и возраст: </b>{item['Nire_date']}\n<b>Тренер команды:</b> {item['Type_club']}
                        """
            text_list.append(text)  # добовление в список
    text_full = "\n".join(text for text in text_list)
    return text_full  # получения списка результатов для пользователя