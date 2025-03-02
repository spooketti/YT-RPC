import asyncio
import websockets
import json
import uuid

connected_clients = {}
broadcasterID = None

async def viewerOfferClient(ws,data,uid):
    global broadcasterID
    if broadcasterID == None:
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

options = {
           "BroadcastReady" : BroadcastReady,
           "viewerOfferClient" : viewerOfferClient,
           "viewerAcceptClient" : viewerAcceptClient,
           "iceToStreamerClient" : iceToStreamerClient,
           "iceToViewerClient" : iceToViewerClient,
}

async def handle_websocket(websocket, path):
    global broadcasterID
    uid = str(uuid.uuid4())
    connected_clients.update({uid:websocket})   
    try:
        async for message in websocket:
            print(f"Received message: {message}")
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
