document.addEventListener('DOMContentLoaded', (event) => {
    const roomId = window.location.pathname.split('/').pop();
    const wsUri = 'ws://' + window.location.host + '/ws/messanger/' + roomId + '/';
    

    const output = document.getElementById('output'); 
    const btnOpen = document.querySelector('.j-btn-open'); 
    const btnSend = document.querySelector('.j-btn-send'); 
    const messageInput = document.getElementById('messageInput');

    if (!btnOpen) {
        console.error('Button with class "j-btn-open" not found.');
        return;
    }

    if (!btnSend) {
        console.error('Button with class "j-btn-send" not found.');
        return;
    }

    let websocket;

    function writeToScreen(message) {
        let pre = document.createElement('p'); 
        pre.style.wordWrap = 'break-word';
        pre.innerHTML = message;
        output.appendChild(pre);
    }

    btnOpen.addEventListener('click', () => {
        websocket = new WebSocket(wsUri); 

        websocket.onopen = function(evt) {
            writeToScreen('Connected'); 
        };

        websocket.onmessage = function(evt) {
            const data = JSON.parse(evt.data);
            writeToScreen('Received: ' + data.user + ': ' + data.message); 
        };

        websocket.onclose = function(evt) {
            writeToScreen('Disconnected'); 
        };

        websocket.onerror = function(evt) {
            writeToScreen('Error: ' + evt.message); 
        };
    });

    btnSend.addEventListener('click', () => {
        if (!websocket || websocket.readyState !== WebSocket.OPEN) {
            writeToScreen('WebSocket is not connected.');
            return;
        }
        const message = messageInput.value;
        websocket.send(JSON.stringify({'message': message}));
        writeToScreen('Sent: ' + message);
        messageInput.value = ''; // Очищаем поле ввода после отправки
    });
});
