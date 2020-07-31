
document.addEventListener('DOMContentLoaded', () => {

  // By default, submit button is disabled
    document.querySelector('#send-button').disabled = true;

  // Enable button only if there is text in the input field
    document.querySelector('#message').onkeyup = () => {
        if (document.querySelector('#message').value.length > 0)
          document.querySelector('#send-button').disabled = false;
        else
          document.querySelector('#send-button').disabled = true;
    };

  //connecting to the websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  //configure buttons after connecting to the socket
  socket.on('connect', () => {

    socket.emit("joined");

    document.querySelector('#message').addEventListener("keydown", event => {
    if (event.key == "Enter") {
        document.getElementById("send-button").click();
    }
});

    document.querySelector('#send-button').addEventListener("click", () => {

      let timestamp = new Date;
      timestamp = timestamp.toLocaleTimeString();

      const message = document.getElementById("message").value;

      socket.emit('submit message', message, timestamp);


    });
  });

  socket.on("display message", data => {

    let row = '<' + `${data.timestamp}` + '> - ' + '[' + `${data.username}` + ']:  ' + `${data.message}`
    document.querySelector("#chat").value += row + '\n'

  })

  socket.on("join message", data => {

    let row = '<' + `${data.message}` + '>'
    document.querySelector('#chat').value += row + '\n';

  })

});

/*
//creating new list element
const li = document.createElement('li');
li.innerHTML = document.querySelector("#message").value;

//adding list item to the list
document.querySelector("#messages").append(li);

//clear the message field and redisable send button
document.querySelector('#submitmessagebutton').disabled = true;
document.querySelector('#message').value = '';

// return false
return false;

*/
