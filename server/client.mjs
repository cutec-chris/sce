import Network from "/server/server/wsclient.mjs"
function InitScene() {
}
global.Network = new Network('ws://localhost:8080/clientsocket')
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
    document.getElementById('nologin').style.display='inline';
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