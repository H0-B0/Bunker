import sys
import os
# Добавляем текущую папку в путь поиска модулей – важно для PyInstaller
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Игроки которые проголосовали
golosa = 0

# Сейчас бесполезно, но когда будет глобальный сервер, будет полезно. Будет выглядеть Код:Вся инфа комнаты
roomses = {}

#Список неизгнанных игроков
array = []

#Цифры - игроки, за чьи номера нельзя встать
players = []

#Локи - Тут у игроков будет последний лок. Напротив номера игрока заблокированная характеристика удаляющая чекбокс
locks = {}

#Все условия сыгранные игроками
uslovies = []

#Игрок:Количество голосов
voices = {}

#Логи, где записано какой игрок за какого проголосовал
logs = []

#Переменная последнего изгнанного игрока
last = 0

class Locks(BaseModel):
    locks:dict

class Player(BaseModel):
    player:int

class RoomData(BaseModel):
    play: dict

class CardUpdate(BaseModel):
    player: str
    card: str
    value: str

class Array(BaseModel):
    array: list

class EveryChar(BaseModel):
    character:str
    players:list
    char_number:int
    text:str

class DealChar(BaseModel):
    player1:str
    player2:str
    char:str
    text:str

class OnlyTwoPlayers(BaseModel):
    player1:str
    player2:str
    text:str

class OpenChar(BaseModel):
    player:str
    character:str
    players:list
    char_number:int
    text:str

class AddVoice(BaseModel):
    player1:int
    player2:int

# Механика создания комнаты
@app.post("/rooms/{room_code}")
async def create_room(room_code: str, data: RoomData):
    print(f'Комната {room_code} создана')
    print(f'Данные: {data.play}')
    roomses[room_code] = data.play
    return {"status": "ok", "message": f"Комната {room_code} успешно создана"}

@app.post('/rooms/{room_code}/voicess')
async def post_voices(room_code:str, data:RoomData):
    global voices
    voices = {}
    keys = list(data.play.keys())
    values = list(data.play.values())
    for key in range(len(keys)):
        voices[int(keys[key])] = int(values[key])
    print(voices)

@app.post('/rooms/{room_code}/locks')
async def add_locks(room_code:str, data:Locks):
    global locks
    locks = data.locks
    print(f'Принят локс: {locks}')

# Механика обновления характеристики у игрока
@app.post("/rooms/{room_code}/update")
async def update_room(room_code: str, data: CardUpdate):
    if room_code not in roomses:
        return {'status': 404, 'message': 'Комната не найдена'}
    if data.player not in roomses[room_code]:
        return {'status': 404, 'message': 'Игрок не найден'}
    roomses[room_code][data.player][data.card] = data.value
    return {'status': 200, 'message': 'OK'}

@app.get("/rooms/{room_code}")
async def show_room(room_code: str):
    if room_code not in roomses:
        return {'status': 404, 'message': 'Комната не найдена'}
    return roomses[room_code]

@app.get('/rooms')
async def show_rooms():
    return list(roomses.keys())

# Механика соответствия количества игроков
@app.post("/rooms/{room_code}/spisok")
async def post_array(room_code:str, data:Array):
    global array
    array = data.array
    print(f'Получен список {array}')

@app.get("/rooms/{room_code}/spisok")
async def get_array():
    print(f'Отправлен список {array}')
    return array


async def izgnat():
    global last
    global logs
    global golosa
    keys = list(voices.keys())
    first_values = list(voices.values())
    values = []
    try:
        for i in first_values:
            values.append(int(i))
    except ValueError: 
        values.append(0)
    max_voice = max(values)
    count = values.count(max_voice)
    if last > 1:
        if len(array)+1 == golosa:
            if count == 1:
                array.remove(keys[values.index(max_voice)])
                print(f'Из эррея удален игрок {keys[values.index(max_voice)]}')
                print(f'Эррей сейчас - {array}')
                golosa = 0
                logs = []
                last = keys[values.index(max_voice)]
                for i in range(min(array),max(array)+1):
                    voices[i] = 0
                voices[keys[values.index(max_voice)]] = 'Изгнан'
                print(voices)

    elif last == 0:
        if len(array) == golosa:
            if count == 1:
                array.remove(keys[values.index(max_voice)])
                print(f'Из эррея удален игрок {keys[values.index(max_voice)]}')
                print(f'Эррей сейчас - {array}')
                golosa = 0
                logs = []
                last = keys[values.index(max_voice)]
                for i in range(min(array),max(array)+1):
                    voices[i] = 0
                voices[keys[values.index(max_voice)]] = 'Изгнан'
                print(voices)

@app.get('/rooms/{room_code}/last')
async def return_last(room_code:str):
    return last

# Механики для добавления/удаления голосов
@app.post('/rooms/{room_code}/voice_a')
async def voice_for_player(room_code:str, data:AddVoice):
    global golosa
    print(f'Добавлен лог: {data.player1}:{data.player2}')

    logs.append({data.player1:data.player2})
    print(f'Логи сейчас: {logs}')

    if data.player2 not in voices:
        voices[data.player2] = 1
    else:
        voices[data.player2] += 1
    print(f'У игрока {data.player2} {voices[data.player2]} голосов')
    print(voices)

    golosa += 1

    print(f'Игроки проголосовавшие сейчас: {golosa}')
    await izgnat()

@app.post('/rooms/{room_code}/voice_d')
async def del_voice_of_player(room_code:str, data:Player):
    global golosa
    global voices
    log = {}

    for index in logs:
        if data.player in index:
            log = index
            print(f'Удален лог {log}')
            logs.remove(index)

    person = list(log.values())[0]
    voices[person] -= 1

    golosa -= 1

    print(f'Игроков проголосовавших сейчас: {golosa}')

    print(f'Логи сейчас: {logs}')

@app.get('/rooms/{room_code}/voice_p')
async def get_voices(room_code:str):
    print(f'Отправлены голоса - {voices}')
    return voices

@app.get('/rooms/{room_code}/igroks')
async def get_igroks(room_code:str):
    return golosa

# Механика удержания номера за игроком
@app.post("/rooms/{room_code}/players/del")
async def del_player(room_code:str, data:Player):
    players.remove(data.player)
    print(f'Удален игрок {data.player}')

@app.post("/rooms/{room_code}/players/accept")
async def accept_player(room_code:str, data:Player):
    players.append(data.player)
    print(f"Принят игрок {data.player}")

@app.get("/rooms/{room_code}/players")
async def get_players(room_code:str):
    print(players)
    return players

# Механика условий

@app.post('/rooms/{room_code}/uslovie/every')
async def every_char(room_code:str, data:EveryChar):
    # Если говорить коротко, то вся эта часть чисто для того, чтобы найти минимальное количество hidden у неизганных игроков
    room_players = roomses[room_code]
    hidden_counts = {}
    schet = 1
    for player in room_players:
        for char in room_players[player]:
            if schet in array:
                if room_players[player][char] == 'hidden':
                    if player not in hidden_counts:
                        hidden_counts[player] = 1
                    else:
                        hidden_counts[player] += 1
        schet += 1
    # Тут мы порсто засовываем в переменную, чтобы было удобно использовать
    min_hidden = min(hidden_counts.values())

    # А тут, если эта характеристика открыта, то ничего не делаем, а если закрыта делаем ее открытой и ставим в локс, чтобы потом убрать чекбокс у игрока, чтобы он не скрыл ее у себя
    for player in hidden_counts.keys():
        if hidden_counts[player] > min_hidden:
            if room_players[player][data.character] == 'hidden':
                locks[player] = data.character
                igrok = int(player.replace('igrok',''))
                roomses[room_code][player][data.character] = data.players[igrok-1][data.char_number]

    print(f'Лок обновлен: {locks}')
    uslovies.append(data.text)

@app.get('/rooms/{room_code}/uslovie/locks')
async def get_locks(room_code:str):
    print(f'Отправлены локи: {locks}')
    return locks

@app.post('/rooms/{room_code}/uslovie/char')
async def deal_one_char(room_code: str, data: DealChar):
    print(f'Приняты игроки {data.player1} и {data.player2}')

    player_one_char = roomses[room_code][data.player1][data.char]
    player_two_char = roomses[room_code][data.player2][data.char]

    print(f'Характеристики игрока 1 - {player_one_char}')
    print(f'Характеристики игрока 2 - {player_two_char}')

    # Если у кого-то hidden — не меняем
    if player_one_char == 'hidden' or player_two_char == 'hidden':
        print('Одна из характеристик скрыта — обмен невозможен')
        return

    # Меняем местами
    roomses[room_code][data.player1][data.char] = player_two_char
    roomses[room_code][data.player2][data.char] = player_one_char

    # Правильные выводы
    print(f'Теперь у {data.player1} характеристика: {roomses[room_code][data.player1][data.char]}')
    print(f'Теперь у {data.player2} характеристика: {roomses[room_code][data.player2][data.char]}')

    print(f'''Полный список:
{roomses[room_code]}''')

    locks[data.player1] = data.char
    locks[data.player2] = data.char
    uslovies.append(data.text)

@app.post('/rooms/{room_code}/uslovie/age')
async def deal_age(room_code:str, data:OnlyTwoPlayers):
    player1 = f'igrok{data.player1}'
    player2 = f'igrok{data.player2}'
    print(f'Приняты игроки {player1} и {player2}')
    print(f'''Биология {player1} игрока - {roomses[room_code][player1]['Биология']}
Биология {player2} игрока - {roomses[room_code][player2]['Биология']}''')
    if roomses[room_code][player1]['Биология'] == 'hidden' or roomses[room_code][player2]['Биология'] == 'hidden': print('Обмен невозможен')
    else:
        age = roomses[room_code][player2]['Биология'].split()[1]
        first_age = roomses[room_code][player1]['Биология'].split()
        first_age[1] = age
        new_biology = ' '.join(first_age)
        roomses[room_code][player1]['Биология'] = new_biology
        print(f'Новая биология {player1} игрока - {roomses[room_code][player1]['Биология']}')
    uslovies.append(data.text)

@app.post('/rooms/{room_code}/uslovie/child')
async def get_child(room_code:str, data:OnlyTwoPlayers):
    player1 = f'igrok{data.player1}'
    player2 = f'igrok{data.player2}'
    print(f'Приняты игроки {player1} и {player2}')
    print(f'''Биология {player1} игрока - {roomses[room_code][player1]['Биология']}
Биология {player2} игрока - {roomses[room_code][player2]['Биология']}''')
    if roomses[room_code][player2]['Биология'] == 'hidden' or roomses[room_code][player1]['Биология'] == 'hidden':
        print('Надо было открыть сначала')
    else:
        bio = roomses[room_code][player2]['Биология'].split()
        if 'Женщина' in bio[0]:
            print(f'{player2} подходит для оплодотворения')
            gender = f'{bio[0]} беременна,'
            bio[0] = gender
            new_bio = ' '.join(bio)
            roomses[room_code][player2]['Биология'] = new_bio
        else:
            print('Брат, это мужик')
    uslovies.append(data.text)

@app.get('/rooms/{room_code}/uslovie/last')
async def play_last_card(room_code:str):
    print(uslovies[-1])
    return uslovies[-1]

@app.post('/rooms/{room_code}/uslovie/open')
async def open_char(room_code:str, data:OpenChar):
    print(f'Данные будут открыты у игрока {data.player}')
    number = int(data.player.replace('igrok',''))
    char = data.players[number-1][data.char_number]
    print(f'Будет взята характеристика {data.character}')
    print(f'Старая характеристика игрока - {roomses[room_code][data.player][data.character]}')
    roomses[room_code][data.player][data.character] = char
    print(f'Новая характеристика игрока - {roomses[room_code][data.player][data.character]}')
    uslovies.append(data.text)
    locks[data.player] = data.character

@app.post('/rooms/{room_code}/uslovie/zapret')
async def close_uslovie(room_code:str, data:Player):
    igrok = f'igrok{data.player}'
    print(f'Принят игрок {igrok}')
    locks[igrok] = 'Условие'
    print(f'У игрока {igrok} заблокировано условие')
    uslovies.append("Запрети использовать карту условия")


@app.post('/rooms/{room_code}/uslovie/gender')
async def change_gender(room_code:str, data:Player):
    player = f'igrok{data.player}'
    if roomses[room_code][player]['Биология'] == 'hidden':
        print('Биология скрыта. ГГ')
        return
    else:
        bio = roomses[room_code][player]['Биология']
        if 'Мужчина' in bio:
            if 'гей' in bio:
                roomses[room_code][player]['Биология'] = bio.replace('Мужчина-гей', 'Женщина-лесбиянка')
            else:
                roomses[room_code][player]['Биология'] = bio.replace('Мужчина', 'Женщина')

            print('Трансформация успешна')
        elif 'Женщина' in bio:
            if 'беременна' in bio:
                print('Трансформация невозможна, беременных мужиков не бывает')
            else:
                if 'лесбиянка' in bio:
                    roomses[room_code][player]['Биология'] = bio.replace('Женщина-лесбиянка', 'Мужчина-гей')
                else:
                    roomses[room_code][player]['Биология'] = bio.replace('Женщина', 'Мужчина')
                    print('Трансформация получилась')
        locks[player] = 'Биология'
    uslovies.append("Измени пол себе или другому игроку")


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)