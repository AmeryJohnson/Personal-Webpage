var socket;
$(document).ready(function () {

    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function () {
        socket.emit('joined', {});
    });

    socket.on('status', function (data) {
        let tag = document.createElement("p");
        let text = document.createTextNode(data.msg);
        let element = document.getElementById("chat");
        tag.appendChild(text);
        tag.style.cssText = data.style;
        element.appendChild(tag);
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });

    socket.on('message', function (data) {
        let tag = document.createElement("p");
        let text = document.createTextNode(data.msg);
        let element = document.getElementById("chat");
        tag.appendChild(text);
        tag.style.cssText = data.style;
        element.appendChild(tag);
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });

    socket.on('left', function (data) {
        let tag = document.createElement("p");
        let text = document.createTextNode(data.msg);
        let element = document.getElementById("chat");
        tag.appendChild(text);
        tag.style.cssText = data.style;
        element.appendChild(tag);
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });

    // Sends a message when pressing Enter key
    $("#message-input").keypress(function (event) {
        if (event.which === 13) {
            event.preventDefault();
            sendMessage();
        }
    });
});

function sendMessage() {
    let message = $("#message-input").val();
    if (message.trim() !== "") {
        socket.emit('text', {'msg': message});
        $("#message-input").val("");
    }
}

function leaveChat() {
    socket.emit('left', {});
    window.location.href = '/home';  // Redirects to the homepage
}

// Disables typing in the chat box
document.getElementById('chat').addEventListener('keypress', function (event) {
    event.preventDefault();
});
