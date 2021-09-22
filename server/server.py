#!/usr/bin/env python
import asyncio,websockets,json,base64,importlib,importlib.util,argparse,logging,pathlib,sys,os
try:import watchdog.observers,watchdog.events
except BaseException as e:logging.debug('Failed importing watchdog:'+str(e))
def getFile(path):
    path = pathlib.Path(path)
    if path.exists():
        with open(str(path),'r') as f:
            return f.read()
    else:
        return None
global ProxySocket 
ProxySocket = None
async def ProcessMessages(uri,args):
    global ProxySocket
    logging.info('connecting to {}'.format(uri))
    async with websockets.connect(uri) as socket:
        ProxySocket = socket
        await socket.send(json.dumps({
                    'method': 'register',
                    'world': args.world,
                }))
        registered = json.loads(await socket.recv())
        if registered['status']!=200:
            return False
        #load World
        try:
            logging.info('loading world %s' % args.world)
            spec = importlib.util.spec_from_file_location(args.world, pathlib.Path(__file__).parent.parent / 'contents' / args.world / '__init__.py')
            w = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(w)
            World = w.World(str(args.savefiles).replace('$world',args.world))
        except BaseException as e:
            logging.error('failed loading World:'+str(e))
            raise
        logging.info('server running')
        try:
            while True:
                umessage = await socket.recv()
                message = json.loads(umessage)
                logging.debug(message)
                if message['method'] == 'get':
                    message['status'] = 200
                    data = getFile(message['uri'])
                    if type(data) is str:
                        data = data.encode()
                    if data is not None:
                        message['data'] = base64.encodebytes(data).decode()
                    else:
                        message['status'] = 404
                    await socket.send(json.dumps(message))
                elif message['method'] == 'login':
                    message['status'] = 200
                    await socket.send(json.dumps(message))
                elif message['method'] == 'register':
                    message['status'] = 200
                    await socket.send(json.dumps(message))
        except asyncio.exceptions.CancelledError:
            pass
        except BaseException as e:
            logging.error(str(e))
async def Watchfiles():
    global ShouldExit
    ShouldExit = False
    try:
        path = pathlib.Path(__file__).parent.parent / 'contents'
        class FileChanged(watchdog.events.FileSystemEventHandler):
            def on_any_event(self,  event):
                global ShouldExit
                if os.path.splitext(event.src_path)[1]=='.py':
                    logging.warning('%s canged, restarting...' % event.src_path)
                    ShouldExit = True
        event_handler = FileChanged()
        observer = watchdog.observers.Observer()
        observer.schedule(event_handler, path, recursive=True)
        logging.info('starting watchdog...')
        observer.start()
        while not ShouldExit:
            await asyncio.sleep(0.1)
    except asyncio.exceptions.CancelledError:
        pass
    except BaseException as e:
        logging.error('Watchdog:'+str(e.__class__)+' '+str(e))
    finally:
        logging.info('finishing watchdog...')
        observer.stop()
        observer.join()
    exec_t = ' '.join([sys.executable, os.path.abspath(__file__), *sys.argv[1:],'&'])
    #print(exec_t)
    #os.system(exec_t)
    raise Exception('file changes')
async def main():
    parser = argparse.ArgumentParser(description='Second Chance Evolution Server.')
    parser.add_argument('proxy', help='The proxy server')
    parser.add_argument('world', help='The directory contains the simulated world')
    parser.add_argument('--savefiles', help='The directory contains the savefiles',default='./savefiles/$world')
    #parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')
    args = parser.parse_args()
    #print(args.accumulate(args.integers))    
    uri = args.proxy+'/serversocket'
    taskMessages = asyncio.Task(ProcessMessages(uri,args))
    taskWatchdog = asyncio.Task(Watchfiles())
    try:
        await asyncio.gather(taskMessages, taskWatchdog)
    except Exception as e:
        taskMessages.cancel()
        taskWatchdog.cancel()
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
ColoredOutput(logging.DEBUG)
logging.getLogger('asyncio').setLevel(logging.ERROR)
logging.getLogger('asyncio.coroutines').setLevel(logging.ERROR)
logging.getLogger('websockets.server').setLevel(logging.ERROR)
logging.getLogger('websockets.protocol').setLevel(logging.ERROR)
asyncio.get_event_loop().run_until_complete(main())