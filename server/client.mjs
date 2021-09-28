import Network from "/server/server/wsclient.mjs"
function InitScene() {
}
global.Network = new Network('ws://localhost:8080/clientsocket')
global.Network.Receive = function(message) {
  //console.log('Received:',message);
  switch(message.action) {
    case 'create-tile':
      newTile = document.getElementById('tiles').appendChild('a-entity');
      newTile.setAttribute('position',message.position);
      newTile.id = message.entityId;
      message.status = 200;
      break;
    case 'destroy-tile':
      aTile = document.getElementById(message.entityId);
      aTile.remove()
      message.status = 200;
      break;
    case 'spawn':
      aParent = document.getElementById(message.parentId);
      break;
    case 'status':
      aObj = document.getElementById(message.entityId);
      break;
  }
  if (message.status == 200) {
    message.to = message.from;
    message.from = global.Network.from;
  }
}
global.Network.Connect = function() {
    function getCookie(cname) {
      let name = cname + "=";
      let decodedCookie = decodeURIComponent(document.cookie);
      let ca = decodedCookie.split(';');
      for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
          c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
          return c.substring(name.length, c.length);
        }
      }
      return "";
    }
    global.Network.SendReceive({
      method: "registration",
      type: "client",
      date: Date.now(),
      from: getCookie('sid')
    },function(msg){
      global.Network.from = msg.to;
      InitScene();
      document.getElementById('scene').style.display='inline';
      document.getElementById('nologin').classList.toggle('fadeout');
      document.getElementById('connectionlost').setAttribute('visible',false);
      window.setTimeout(() => {
        document.getElementById('nologin').style.display='none';
      }, 1000);
    });
}
global.Network.Disconnect = function() {
  document.getElementById('connectionlost').setAttribute('visible',true)
}