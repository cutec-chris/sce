import Network from "/server/server/wsclient.mjs"
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
    global.Network.SendReceive({
      method: "registration",
      type: "client",
      date: Date.now(),
      from: getCookie('sid')
    },function(msg){
      global.Network.from = msg.to;
      document.getElementById('connectionlost').setAttribute('visible',false)
    });
}
global.Network.Connect = function() {
  document.getElementById('connectionlost').setAttribute('visible',true)
}