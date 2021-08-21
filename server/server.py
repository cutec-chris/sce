#!/usr/bin/env python
import asyncio,websockets,json,base64
def getFile(path):
    return 'Hello World from '+path
async def main():
    uri = "ws://localhost:8080/serversocket"
    async with websockets.connect(uri) as socket:
        await socket.send(json.dumps({
                    'method': 'register',
                }))
        registered = json.loads(await socket.recv())
        if registered['status']!=200:
            return False
        while True:
            umessage = await socket.recv()
            message = json.loads(umessage)
            if message['method'] == 'get':
                message['status'] = 200
                data = getFile(message['uri'])
                if type(data) is str:
                    data = data.encode()
                message['data'] = base64.encodebytes(data).decode()
                await socket.send(json.dumps(message))
asyncio.get_event_loop().run_until_complete(main())