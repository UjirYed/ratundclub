document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure button
    socket.on('connect', () => {

        // Notify the server user has joined
        socket.emit('joined');
        // 'Enter' key on textarea also sends a message
        // https://developer.mozilla.org/en-US/docs/Web/Events/keydown
        document.querySelector('#message').addEventListener("keydown", event => {
            if (event.key == "Enter") {
                document.getElementById("send-button").click();
            }
        });

        // Send button emits a "message sent" event
        document.querySelector('#send-button').addEventListener("click", () => {

            // Save time in format HH:MM:SS
            let timestamp = new Date;
            timestamp = timestamp.toLocaleTimeString();

            // Save user input
            let message = document.getElementById("message").value;

            socket.emit('submit message', message, timestamp);

            // Clear input
            document.getElementById("message").value = '';
        });
    });

    // When user joins a channel, add a message and on users connected.
    socket.on('status', data => {

        // Broadcast message of joined user.
        let row = '<' + `${data.message}` + '>'
        document.querySelector('#chat').value += row + '\n';
    })

    // When a message is announced, add it to the textarea.
    socket.on('display message', data => {

        // Format message
        let row = '<' + `${data.timestamp}` + '> - ' + '[' + `${data.user}` + ']:  ' + `${data.message}`
        document.querySelector('#chat').value += row + '\n'
    })


});
