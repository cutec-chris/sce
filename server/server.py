#!/usr/bin/env python
import asyncio,websockets,json,base64,importlib,argparse,logging
def getFile(path):
    return 'Hello World from '+path
async def main():
    parser = argparse.ArgumentParser(description='Second Chance Evolution Server.')
    parser.add_argument('proxy', help='The proxy server')
    parser.add_argument('world', help='The directory contains the simulated world')
    #parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')
    args = parser.parse_args()
    #print(args.accumulate(args.integers))    
    uri = args.proxy+'/serversocket'
    logging.warning('connecting to {}'.format(uri))
    try:
        async with websockets.connect(uri) as socket:
            await socket.send(json.dumps({
                        'method': 'register',
                    }))
            registered = json.loads(await socket.recv())
            if registered['status']!=200:
                return False
            #load World
            w = importlib.import_module('.'+args.world,'..contents')
            World = w.World
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
    except: logging.error('Server connection failed.')
asyncio.get_event_loop().run_until_complete(main())