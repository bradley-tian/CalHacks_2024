import asyncio
import websockets
import json

DEEPGRAM_API_KEY = "dfa7a4af38edb4a9ea1e7969e2ef192c9bb4c213"
DEEPGRAM_WS_URL = "wss://agent.deepgram.com/agent"

headers = {
    "Authorization": f"Token {DEEPGRAM_API_KEY}",
    "Content-Type": "application/json"
}

def to_binary(s):
    s = ''.join(s.split())
    if len(s) % 8 != 0:
        raise ValueError("Length of binary string must be a multiple of 8.")
    return bytes(int(s[i:i+8], 2) for i in range(0, len(s), 8))

async def handler(ws, path):
    print("WebSocket connection established")
    
    try:

        async with websockets.connect(DEEPGRAM_WS_URL, extra_headers=headers) as deepgram_ws:
            print("Connected to Deepgram WebSocket")
            
            config = json.load(open("config.json"))
            await deepgram_ws.send(json.dumps(config))

            print("Sent configuration to Deepgram")

            async def receive_from_client():
                async for message in ws:
                    if isinstance(message, bytes):
                        print(f"Forwarding binary data to Deepgram")
                        await deepgram_ws.send(message)
                    else:
                        print(f"Forwarding text message to Deepgram: {to_binary(message)}")
                        await deepgram_ws.send(to_binary(message))

            async def receive_from_deepgram():
                async for message in deepgram_ws:
                    print(f"Received from Deepgram: {message}")
                    await ws.send(message)

            await asyncio.gather(
                receive_from_client(),
                receive_from_deepgram()
            )

    except Exception as e:
        print(f"WebSocket connection error: {e}")
        await ws.close()

async def main():
    server = await websockets.serve(handler, "localhost", 8765)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())