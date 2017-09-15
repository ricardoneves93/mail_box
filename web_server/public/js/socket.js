var ws;
		    
function init() {

  // Connect to Web Socket
  ws = new WebSocket("ws://192.168.2.103:8081/");

  var re = new RegExp('new_mail_*');

  // Set event handlers.
  ws.onopen = function() {
    console.log("onopen");
  };
  
  ws.onmessage = function(e) {
    // e.data contains received string.
    console.log("onmessage: " + e.data);
    var message = e.data;
    if(message.match(re) != null) {
    	$("#mail_status").css("background-color", "green");
      console.log(message.split('_')[2]);
      $(".message-counter").html(message.split('_')[2]);
      ion.sound.play("door_bell");
      //document.getElementById("sound").innerHTML='<audio autoplay="autoplay"><source src="sound/pacman.mp3" type="audio/mpeg" /><embed hidden="true" autostart="true" loop="false" src="sound/pacman.mp3" /></audio>';
    }
    else if(message == "open_door") {
      $("#mail_status").css("background-color", "red");
    	$("#door_status").css("background-color", "green");
      $("#door_status_img").attr('src', 'img/open_door.png')
      $(".message-counter").html(0);
    }
    else if(message == "close_door") {
    	$("#door_status").css("background-color", "red");
      $("#door_status_img").attr('src', 'img/close_door.png')
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
