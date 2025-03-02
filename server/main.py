import asyncio
import websockets

# Define a callback function to handle incoming WebSocket messages
async def handle_websocket(websocket, path):
    try:
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")

            # You can send a response back to the client if needed
            response = f"Received: {message}"
            await websocket.send(response)
    except websockets.ConnectionClosed:
        pass


server = websockets.serve(handle_websocket, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()