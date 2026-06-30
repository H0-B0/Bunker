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

# Механика создания комнаты
@app.post("/rooms/{room_code}")
async def create_room(room_code: str, data: RoomData):
    print(f'Комната {room_code} создана')
    print(f'Данные: {data.play}')
    roomses[room_code] = data
    return {"status": "ok", "message": f"Комната {room_code} успешно создана"}

# Механика обновления характеристики у игрока
@app.post("/rooms/{room_code}/update")
async def update_room(room_code: str, data: CardUpdate):
    if room_code not in roomses:
        return {'status': 404, 'message': 'Комната не найдена'}
    if data.player not in roomses[room_code].play:
        return {'status': 404, 'message': 'Игрок не найден'}
    roomses[room_code].play[data.player][data.card] = data.value
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

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)