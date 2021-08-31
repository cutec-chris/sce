import bottle,json,logging,base64,random,time,pathlib,os
app = bottle.Bottle()
servers = []
@app.route('/')
@app.route('/index.html')
@app.route('/client/<filepath>')
def handle_index(filepath='index.html'):
    basepath = str(pathlib.Path('/'.join(list(pathlib.Path(__file__).parts)[0:-2])) / 'client')
    if os.path.splitext(filepath)[1][:4].lower() == '.htm':
        return bottle.jinja2_template(filepath,template_lookup=[basepath])
    else:
        return bottle.static_file(filepath,basepath)
def sendrec(message,sock):
    aId = int(random.random()*10000)
    message['id'] = aId
    try:
        sock.send(json.dumps(message))
        for i in range(1000):
            for msg in sock.environ['messages']:
                if msg['id'] == aId:
                    res = msg
                    sock.environ['messages'].remove(msg)
                    return msg
            gevent.sleep(0.0001)
    except:
        pass
    return None    
@app.route('/server/<filepath>')
def handle_file(filepath):
    if len(servers) == 0:
        bottle.abort(502,'No servers avalible')
    for server in servers:
        answer = sendrec({
            'method': 'get',
            'uri': filepath
            },server)
        if answer and answer['status']==200:
            return base64.decodebytes(answer['data'].encode())
            break
    return bottle.abort(404)
@app.route('/serversocket')
def handle_server():
    wsock = bottle.request.environ.get('wsgi.websocket')
    if not wsock:
        bottle.abort(400, 'Expected WebSocket request.')
    reg = json.loads(wsock.receive())
    reg['status'] = 200
    wsock.send(json.dumps(reg))
    wsock.environ['messages'] = []
    servers.append(wsock)
    logging.info('new server:'+str(wsock.environ['REMOTE_ADDR']))
    while True:
        try:
            message = wsock.receive()
            if message:
                wsock.environ['messages'].append(json.loads(message))
        except WebSocketError:
            break
    logging.info('server gone')
    servers.remove(wsock)
@app.route('/clientsocket')
def handle_client():
    wsock = bottle.request.environ.get('wsgi.websocket')
    if not wsock:
        bottle.abort(400, 'Expected WebSocket request.')
    while True:
        try:
            message = wsock.receive()
            #wsock.send("Your message was: %r" % message)
        except WebSocketError:
            break
import gevent.monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
logging.basicConfig(level=logging.INFO)
server = WSGIServer(("0.0.0.0", 8080), app,
                    handler_class=WebSocketHandler)
server.serve_forever()