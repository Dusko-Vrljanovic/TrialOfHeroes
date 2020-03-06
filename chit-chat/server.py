import random

import socketio
import uvicorn

sio = socketio.AsyncServer()
app = socketio.ASGIApp(sio, static_files = {
    "/" : "index.html"
})


@sio.event
async def connect(sid, environ):
    username = "RandomUser" + str(random.randint(0, 1000000))
    room = "global"
    await sio.save_session(sid, {"username": username, "room": room})
    
    sio.enter_room(sid, room)
    await sio.emit("user_joined", username, room=room, skip_sid=sid)

@sio.event
async def disconnect(sid):
    session = await sio.get_session(sid)
    username = session["username"]
    room = session["room"]

    sio.leave_room(sid, room)
    await sio.emit("user_left", username, room=room, skip_sid=sid)

@sio.on("send_message")
async def message_recieved(sid, data):
    session = await sio.get_session(sid)
    username = session["username"]
    room = session["room"]

    await sio.emit("on_message", "{}: {}".format(username, data["msg"]), room=room, skip_sid=sid)





