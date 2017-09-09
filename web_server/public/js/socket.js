var ws;
		    
function init() {

  // Connect to Web Socket
  ws = new WebSocket("ws://192.168.2.103:8081/");

  // Set event handlers.
  ws.onopen = function() {
    console.log("onopen");
  };
  
  ws.onmessage = function(e) {
    // e.data contains received string.
    console.log("onmessage: " + e.data);
    var message = e.data;
    if(message == "new_mail") {
    	$("#mail_status").css("background-color", "green");
    }
    else if(message == "open_door") {
    	$("#mail_status").css("background-color", "red");
    }
    else if(message == "close_door") {
    	//alert("A porta está fechada");
    }

  };
  
  ws.onclose = function() {
    console.log("onclose");
  };

  ws.onerror = function(e) {
    console.log("onerror");
    console.log(e)
  };

}
