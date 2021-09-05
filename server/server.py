#!/usr/bin/env python
import asyncio,websockets,json,base64,importlib,importlib.util,argparse,logging,pathlib,sys,os
try:import watchdog.observers,watchdog.events
except BaseException as e:logging.debug(str(e))
def getFile(path):
    if str(path).startswith('/world/'):
        return 'Hello from World '+path
    else:
        return 'Hello World from '+path
async def main():
    parser = argparse.ArgumentParser(description='Second Chance Evolution Server.')
    parser.add_argument('proxy', help='The proxy server')
    parser.add_argument('world', help='The directory contains the simulated world')
    parser.add_argument('--savefiles', help='The directory contains the savefiles',default='./savefiles/$world')
    #parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')
    args = parser.parse_args()
    #print(args.accumulate(args.integers))    
    uri = args.proxy+':8080/serversocket'
    logging.info('connecting to {}'.format(uri))
    try:
        async with websockets.connect(uri) as socket:
            await socket.send(json.dumps({
                        'method': 'register',
                    }))
            registered = json.loads(await socket.recv())
            if registered['status']!=200:
                return False
            #load World
            logging.info('loading world %s' % args.world)
            spec = importlib.util.spec_from_file_location(args.world, pathlib.Path(__file__).parent.parent / 'contents' / args.world / '__init__.py')
            w = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(w)
            World = w.World(str(args.savefiles).replace('$world',args.world))
            logging.info('server running')
            try:
                path = pathlib.Path(__file__).parent.parent / 'contents'
            except BaseException as e: logging.warning('reloading disabled: '+str(e))
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
    except BaseException as e: logging.error('Server connection failed. (%s)' % str(e))
def ColoredOutput(log_level):
    def set_color(level, code):
        level_fmt = "\033[1;" + str(code) + "m%s\033[1;0m" 
        logging.addLevelName( level, level_fmt % logging.getLevelName(level) )
    std_stream = sys.stdout
    isatty = getattr(std_stream, 'isatty', None)
    if isatty and isatty():
        levels = [logging.DEBUG, logging.CRITICAL, logging.WARNING, logging.ERROR]
        set_color(logging.WARNING, 34)
        set_color(logging.ERROR, 31)
        set_color(logging.CRITICAL, 45)
        for idx, level in enumerate(levels):
            set_color(level, 30 + idx )
    logging.basicConfig(stream=std_stream, level=log_level)
    logging.root.setLevel(log_level)    
ColoredOutput(logging.INFO)
asyncio.get_event_loop().run_until_complete(main())