import Network from "../common/wsclient.mjs"
global.Network = new Network('ws://localhost:8080')
global.Network.Connect = function() {
    global.Network.SendReceive({
      action: "registration",
      type: "client",
      date: Date.now()
    },function(msg){
      global.Network.from = msg.to;
      InitScene();
    });
}
