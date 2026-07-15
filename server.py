import sys
import os
# Добавляем текущую папку в путь поиска модулей – важно для PyInstaller
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

roomses = {}

array = []

players = []

locks = {}

uslovies = []

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

# Механика создания комнаты
@app.post("/rooms/{room_code}")
async def create_room(room_code: str, data: RoomData):
    print(f'Комната {room_code} создана')
    print(f'Данные: {data.play}')
    roomses[room_code] = data.play
    return {"status": "ok", "message": f"Комната {room_code} успешно создана"}

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

# Механики для изгнания/ возвращения игроков
@app.post('/rooms/{room_code}/add_player')
async def addPlayer(room_code:str, data:Player):
    global array
    if data.player not in array:
        array.append(data.player)
        print(data.player)
        print(array)

@app.post('/rooms/{room_code}/del_player')
async def delPlayer(room_code:str, data:Player):
    global array
    try:
        array.remove(data.player)
    except Exception as e:
        pass
    print(data.player)
    print(array)

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


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)