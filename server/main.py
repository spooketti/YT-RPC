import asyncio
import websockets
import json
import uuid
import time

#TODO: in the event of making a rooms system: make this not global but this todo basically just means recode YT-RPC and i aint about allat
lastRequestTimestamp = time.time() #time since someone last pushed the button

print("the saints went marching in")
connected_clients = {}
broadcasterID = None

async def viewerOfferClient(ws,data,uid):
    global broadcasterID
    if broadcasterID == None:
        if time.time() - lastRequestTimestamp > 5:
            lastRequestTimestamp = time.time()
            payload = {
                "context":"streamRequest"
                }
            for uid,ws in connected_clients.items():
                await ws.send(json.dumps(payload))
        return
    sdp = data.get("sdp")
    returnSocket = uid
    payload = {
        "sdp":sdp,
        "returnID":returnSocket,
        "context":"viewerOfferServer"
    }
    await connected_clients[broadcasterID].send(json.dumps(payload))
    
async def viewerAcceptClient(ws,data,uid):
    if broadcasterID == None:
        return
    sdp = data.get("sdp")
    returnID = data.get("returnID")
    payload = {
        "sdp":sdp,
        "context":"viewerAcceptServer"
    }
    await connected_clients[returnID].send(json.dumps(payload))

async def iceToStreamerClient(ws,data,uid):
    if broadcasterID == None:
        return
    candidate = data.get("candidate")
    payload = {
        "candidate":candidate,
        "context":"iceToStreamerServer"
    }
    await connected_clients[broadcasterID].send(json.dumps(payload))
    
async def iceToViewerClient(ws,data,uid):
    if broadcasterID == None:
        return
    candidate = data.get("candidate")
    payload = {
        "candidate":candidate,
        "context":"iceToViewerServer"
    }
    for uid,ws in connected_clients.items():
        if(uid == broadcasterID):
            continue
        await ws.send(json.dumps(payload))

async def BroadcastReady(ws,data,uid):
    global broadcasterID
    broadcasterID = uid

def uuidColor(uid:str): 
    realUID = uuid.UUID(uid)
    return f"#{realUID.hex[:6]}"

async def recieveChat(ws,data,clientUID):
    message = data.get("message")
    if not message.strip() or len(message) == 0:
        return
    username = data.get("username")
    if not username.strip() or len(username) == 0:
        username = f"Guest {clientUID[:4]}"
    for uid,ws in connected_clients.items():
        payload = {
        "username":username,
        "message": message,
        "context":"chatSTC",
        "color":uuidColor(clientUID)
    }
        await ws.send(json.dumps(payload))

options = {
           "BroadcastReady" : BroadcastReady,
           "viewerOfferClient" : viewerOfferClient,
           "viewerAcceptClient" : viewerAcceptClient,
           "iceToStreamerClient" : iceToStreamerClient,
           "iceToViewerClient" : iceToViewerClient,
           "chatCTS": recieveChat
}


async def handle_websocket(websocket, path):
    global broadcasterID
    uid = str(uuid.uuid4())
    connected_clients.update({uid:websocket})   
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                print("Invalid JSON received")
                continue
            if(data.get("context") in options):
                await options[data.get("context")](websocket,data,uid)
            
    except websockets.ConnectionClosed:
        print("Client disconnected")
    finally:
        if uid == broadcasterID:
            broadcasterID = None
        del connected_clients[uid]

# Start the WebSocket server
server = websockets.serve(handle_websocket, "0.0.0.0", 8085)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
