from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

roomses = {}

class RoomData(BaseModel):
    play: dict

class CardUpdate(BaseModel):
    player: str
    card: str
    value: str

@app.post("/rooms/{room_code}")
async def create_room(room_code: str, data:RoomData):
    print(f'Комната {room_code} создана')
    print(f'Данные: {data.play}')
    roomses[room_code] = data
    return {"status":"ok", "message":f"Комната {room_code} успешно создана"}

@app.post("/rooms/{room_code}/update")
async def update_room(room_code:str, data:CardUpdate):
    if room_code not in roomses: return {'status':404, 'message':'Комната не найдена'}
    elif roomses[room_code].play.get(data.player) == None: return {'status':404, 'message':'Игрок не найден'}
    else:
        roomses[room_code].play[data.player][data.card] = data.value

    return {'status':200, 'message':'OK'}

@app.get("/rooms/{room_code}")
async def show_room(room_code:str):
    if room_code not in roomses: return {'status':404, 'message':'Комната не найдена'}
    else: 
        return roomses[room_code]
    
@app.get('/rooms')
async def show_rooms():
    return list(roomses.keys())