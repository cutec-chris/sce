import bottle,json,logging,base64,random,time,pathlib,os,uuid,sys
app = bottle.Bottle()
servers = []
users = []
ownId = str(uuid.uuid4())
@app.route('/')
@app.route('/index.html')
@app.route('/client/<filepath:path>')
def handle_index(filepath='index.html'):
    basepath = str(pathlib.Path('/'.join(list(pathlib.Path(__file__).parts)[0:-2])) / 'client')
    if os.path.splitext(filepath)[1][:4].lower() == '.htm':
        return bottle.jinja2_template(filepath,template_lookup=[basepath])
    else:
        return bottle.static_file(filepath,basepath)
def sendrec(message,sock):
    aId = int(random.random()*10000)
    message['id'] = aId
    message['from'] = ownId
    try:
        emsg = json.dumps(message)
        sock.send(emsg)
        for i in range(5000):
            for msg in sock.environ['messages']:
                if msg['id'] == aId:
                    res = msg
                    sock.environ['messages'].remove(msg)
                    return msg
            gevent.sleep(0.001)
    except BaseException as e:
        logging.error(str(e))
    return None    
def FindServer(newUser):
    #find Server with minimal Users count
    MinCnt = 999999
    MinCntServer = None
    for server in servers:
        if not server.closed:
            if not 'userCount' in server.environ or server.environ['userCount'] < MinCnt:
                MinCnt = server.environ['userCount']
                MinCntServer = server
    if MinCntServer:
        answer = sendrec({
            'method': 'login',
            'user': newUser['data']
            },MinCntServer)
        if answer\
        and answer['status'] == 200:
            if not newUser in users:
                users.append(newUser)
            MinCntServer.environ['userCount'] += 1
            if newUser['data']['id'] is None:
                id = str(uuid.uuid4())
                newUser['data']['id'] = id
            newUser['server'] = MinCntServer
            return MinCntServer
    return None
@app.post('/login')
def handle_login():
    newUser = { "data": {
                    "user": bottle.request.forms.get('password'),
                    "password": bottle.request.forms.get('password'),
                    #"challange": bottle.request.forms.get('challange'),
                    "id": None,
                }
            }
    if FindServer(newUser):
        bottle.response.set_cookie('sid',newUser['data']['id'])
        bottle.redirect('/server/contents/'+newUser['server'].environ['reg']['world']+'/world.html')
        logging.info('User %s logged in' % newUser['user'])
    else:
        logging.warning('No server avalible or Login failed')
        try: return bottle.redirect('/')
        except: pass
@app.route('/server/<filepath:path>')
def handle_file(filepath):
    if len(servers) == 0:
        bottle.abort(502,'No servers avalible')
    for server in servers:
        answer = sendrec({
            'method': 'get',
            'uri': filepath
            },server)
        if answer and answer['status']==200:
            if filepath.endswith('.mjs')\
            or filepath.endswith('.js'):
                bottle.response.content_type = 'application/javascript'
            elif filepath.endswith('.css'):
                bottle.response.content_type = 'text/css'
            res = base64.decodebytes(answer['data'].encode())
            bottle.response.headers['Cache-Control'] = 'public, max-age=604800'
            #bottle.response.headers['Cache-Control'] = 'no-cache'
            bottle.response.headers['Last-Modified'] = answer['lastModified']
            bottle.response.content_length = answer['size']
            return res
        elif answer:
            #print(answer)
            return bottle.abort(answer['status'])
    return bottle.error(400)
@app.route('/serversocket')
def handle_server():
    wsock = bottle.request.environ.get('wsgi.websocket')
    if not wsock:
        bottle.abort(400, 'Expected WebSocket request.')
    reg = json.loads(wsock.receive())
    reg['status'] = 200
    wsock.send(json.dumps(reg))
    wsock.environ['reg'] = reg
    wsock.environ['messages'] = []
    wsock.environ['userCount'] = 0
    wsock.environ['users'] = []
    servers.append(wsock)
    logging.info('new server:'+str(wsock.environ['REMOTE_ADDR']))
    while True:
        try:
            message = wsock.receive()
            if message:
                if ownId in message: #answer to proxy
                    wsock.environ['messages'].append(json.loads(message))
                else:               #direct message no answer (or expected)
                    for user in users:
                        if 'id' in user:
                            if user['id'] in message:
                                user['socket'].send(message)
                                break
        except WebSocketError:
            break
    logging.info('server gone')
    for user in users:
        if user['server'] == wsock:
            user['server'] = None
            try: user['socket'].close()
            except: pass
    for server in servers:
        if server.closed:
            servers.remove(wsock)
@app.route('/clientsocket')
def handle_client():
    wsock = bottle.request.environ.get('wsgi.websocket')
    if not wsock:
        bottle.abort(400, 'Expected WebSocket request.')
    #registration
    message = wsock.receive()
    message = json.loads(message)
    res = None
    if message['method'] == 'registration':
        for user in users:
            if user['data']['id'] == message['from']:
                res = message
                wsock.environ['user'] = user
                user['socket'] = wsock
                if wsock.environ['user']['server'] is None:
                    if not FindServer(user):
                        res = None
        if res:
            res['status'] = 200
            res['to'] = res['from']
            res['from'] = None
            tsnd = json.dumps(res)
            wsock.send(tsnd)
            wsock.environ['user']['server'].send(tsnd)
        else:
            return
    while True:
        try:
            message = wsock.receive()
            try:
                #wsock.send("Your message was: %r" % message)
                wsock.environ['user']['server']['socket'].send(message)
                if res:
                    wsock.send(json.dumps(res))
            except:
                pass
        except WebSocketError:
            break
import gevent.monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
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
server = WSGIServer(("0.0.0.0", 8080), app,
                    handler_class=WebSocketHandler)
server.serve_forever()