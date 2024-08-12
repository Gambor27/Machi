from PyP100 import PyL530
import os
import asyncio
import websockets
from dotenv import load_dotenv

def get_rooms():
    load_dotenv()    
    password = os.getenv('PASSWORD')
    email = os.getenv('EMAIL')
    rooms = {"living_room":[PyL530.L530("10.0.0.166", email, password)], "bedroom":[PyL530.L530("10.0.0.136", email, password),PyL530.L530("10.0.0.85", email, password)], "dining_room":[PyL530.L530("10.0.0.187", email, password),PyL530.L530("10.0.0.245", email, password),PyL530.L530("10.0.0.206", email, password)]}
    return rooms

def room_lights_on(rooms, room):
    for bulb in rooms[room]:
        bulb.turnOnWithDelay(1)

def room_lights_off(rooms, room):
    for bulb in rooms[room]:
        bulb.turnOffWithDelay(1)

def set_room_brightness(rooms, room, value):
    for bulb in rooms[room]:
        bulb.setBrightness(value)

def set_room_color(rooms, room, hue, saturation):
    for bulb in rooms[room]:
        bulb.setColor(hue, saturation)

async def handler(websocket, path):
    data = await websocket.recv()
    reply = f"Data recieved as:  {data}!"
    await websocket.send(reply)

def main():
    rooms = get_rooms()
    start_server = websockets.serve(handler, "localhost", 8567)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

main()