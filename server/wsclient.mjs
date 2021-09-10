export default class Network {
    constructor(aServer) {
        this.Server = aServer
        this.reconnectTimeout = 1000
    }
    set Server(aServer) {
        this.Socket = null
        this.onConnect = null;
        this.socketQueueId = 0;
        this.socketQueue = {};
        try {  this.Socket = new window.WebSocket(aServer)
        } catch {
            this.Socket = new global.WebSocket(aServer)
        }
        this.Socket.onopen = function open() {
            console.log('connected');
            if (this.WServer.Connect != null) {
                this.WServer.Connect();
            }
        };
        this.Socket.onclose = function close() {
            console.log('disconnected');
            try { window.setTimeout(this.WServer.doReconnect,this.reconnectTimeout,this.WServer);
            } catch {
                setTimeout(this.WServer.doReconnect,this.reconnectTimeout,this.WServer);
            }
            if (this.WServer.Disconnect != null) {
                this.WServer.Disconnect();
            }
        };
        this.Socket.onmessage = function incoming(data) {
            try {
                var msg = JSON.parse(data.data)
                if (typeof(msg.cmd_id) != 'undefined' && typeof(msg.cmd_id[this.WServer.from]) != 'undefined' && typeof(this.WServer.socketQueue[msg.cmd_id[this.WServer.from]]) == 'function'){
                    var aid = msg.cmd_id[this.WServer.from];
                    var execFunc = this.WServer.socketQueue[aid];
                    delete msg.cmd_id[this.WServer.from];
                    execFunc(msg);
                    delete this.WServer.socketQueue[aid];
                    return;
                }else{
                    if (this.WServer.Receive)
                        this.WServer.Receive(msg);
                }
            } catch (e) {
                console.error('failed to receive msg ',e)
            }
        };
        this.Socket.onerror = function incoming(data) {
            console.log('error:'+data);
        };
        this.Socket.WServer = this;
        this._Server = aServer;
    }
    Send(Message) {
        if (this.from)
          Message.from = this.from;
        this.Socket.send(JSON.stringify(Message))
    }
    SendReceive(msg,Answer) {
        if (this.from)
            msg.from = this.from;
        if (this.token)
            msg.token = this.token;
        this.socketQueueId++;
        if (typeof(Answer) == 'function'){
            // the '_' prefix is a good way to force string indices, believe me you'll want that in case your server side doesn't care and mixes both like PHP might do
            this.socketQueue[this.from+'_'+this.socketQueueId] = Answer;
        }
        if (typeof(msg.cmd_id) == 'undefined') {
            msg.cmd_id = {}
        }
        msg.cmd_id[this.from] = this.from+'_'+this.socketQueueId;
        this.Socket.send(JSON.stringify(msg));
    }
    doReconnect(nw) {
        console.log('reconnecting...')
        nw.Server = nw._Server
    }
    mergeStrings = (a, b) => {
        let s = '';
        for (let i = 0; i < Math.max(a.length, b.length); i++) {
          s += String.fromCharCode(
            (a.charCodeAt(i) || 0) ^ (b.charCodeAt(i) || 0)
          );
        }
        return s;
      };
}
