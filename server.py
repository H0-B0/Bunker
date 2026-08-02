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

class OpenChar(BaseModel):
    player:str
    character:str
    players:list
    char_number:int
    text:str

from typing import Any
class ActionData(BaseModel):
    player: str
    players: Any
    target_player: str | None = None
    selected_trait: str | None = None
    char_index: int | None = None
    card_data: dict
    text: str


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

@app.post('/rooms/{room_code}/execute_action')
async def execute_action(room_code: str, data: ActionData):
    print(f"Executing action: {data.card_data['action']} by {data.player} on {data.target_player}")
    action = data.card_data["action"]
    trait = data.card_data.get("trait") or data.selected_trait
    
    if action == "SWAP_TRAIT":
        player1 = data.player
        player2 = data.target_player
        if roomses[room_code][player1][trait] == 'hidden' or roomses[room_code][player2][trait] == 'hidden':
            print('Обмен невозможен - характеристика скрыта')
            return
        
        temp = roomses[room_code][player1][trait]
        roomses[room_code][player1][trait] = roomses[room_code][player2][trait]
        roomses[room_code][player2][trait] = temp
        locks[player1] = trait
        locks[player2] = trait
        
    elif action == "CHANGE_AGE":
        player1 = data.player
        player2 = data.target_player
        if roomses[room_code][player1]['Биология'] == 'hidden' or roomses[room_code][player2]['Биология'] == 'hidden':
            return
        age = roomses[room_code][player2]['Биология'].split()[1]
        first_age = roomses[room_code][player1]['Биология'].split()
        first_age[1] = age
        roomses[room_code][player1]['Биология'] = ' '.join(first_age)
        
    elif action == "MAKE_PREGNANT":
        player2 = data.target_player
        if roomses[room_code][player2]['Биология'] == 'hidden': return
        bio = roomses[room_code][player2]['Биология'].split()
        if 'Женщина' in bio[0]:
            bio[0] = f'{bio[0]} беременна,'
            roomses[room_code][player2]['Биология'] = ' '.join(bio)
            
    elif action == "CHANGE_GENDER":
        player = data.target_player
        if roomses[room_code][player]['Биология'] == 'hidden': return
        bio = roomses[room_code][player]['Биология']
        if 'Мужчина' in bio:
            if 'гей' in bio: roomses[room_code][player]['Биология'] = bio.replace('Мужчина-гей', 'Женщина-лесбиянка')
            else: roomses[room_code][player]['Биология'] = bio.replace('Мужчина', 'Женщина')
        else:
            if 'беременна' in bio:
                print('Трансформация невозможна, беременных мужиков не бывает')
            else:
                if 'лесбиянка' in bio: roomses[room_code][player]['Биология'] = bio.replace('Женщина-лесбиянка', 'Мужчина-гей')
                else: roomses[room_code][player]['Биология'] = bio.replace('Женщина', 'Мужчина')
        locks[player] = 'Биология'
            
    elif action == "BAN_VOTE":
        locks[data.target_player] = 'Условие'
        
    elif action == "REVEAL_ANY":
        # data.players это список списков
        igrok_num = int(data.target_player.replace('igrok', ''))
        char_val = data.players[igrok_num - 1][data.char_index]
        roomses[room_code][data.target_player][trait] = char_val
        locks[data.target_player] = trait
        
    elif action == "REVEAL_ALL":
        room_players = roomses[room_code]
        hidden_counts = {}
        schet = 1
        for p in room_players:
            for char in room_players[p]:
                if schet in array:
                    if room_players[p][char] == 'hidden':
                        hidden_counts[p] = hidden_counts.get(p, 0) + 1
            schet += 1
        min_hidden = min(hidden_counts.values()) if hidden_counts else 0
        for p in hidden_counts:
            if hidden_counts[p] > min_hidden:
                if room_players[p][trait] == 'hidden':
                    locks[p] = trait
                    igrok = int(p.replace('igrok',''))
                    roomses[room_code][p][trait] = data.players[igrok - 1][data.char_index]
                    
    uslovies.append(data.text)
    return {"status": "success"}

@app.get('/rooms/{room_code}/uslovie/locks')
async def get_locks(room_code:str):
    print(f'Отправлены локи: {locks}')
    return locks

# Removed char, age, child endpoints

@app.get('/rooms/{room_code}/uslovie/last')
async def play_last_card(room_code:str):
    print(uslovies[-1])
    return uslovies[-1]

# Removed open, zapret, gender endpoints


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)