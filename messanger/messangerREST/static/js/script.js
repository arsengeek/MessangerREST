const openWebSocketButton = document.querySelector('#openWebSocket');
const sendMessageButton = document.querySelector('#sendMessage');
const messageInput = document.querySelector('#myInput');
const outputDiv = document.querySelector('#output');
const roomIdElement = document.querySelector('#roomId'); // Получаем элемент с id="roomId"

if (roomIdElement) { // Проверяем, что элемент существует
    const roomId = roomIdElement.textContent.trim();
    let chatSocket;

    openWebSocketButton.onclick = function() {
        if (!chatSocket || chatSocket.readyState === WebSocket.CLOSED) {
            const wsUrl = `ws://${window.location.host}/ws/messanger/${roomId}/`;
            console.log('Connecting to WebSocket:', wsUrl);
            chatSocket = new WebSocket(wsUrl);

            chatSocket.onmessage = function(e) {
                const data = JSON.parse(e.data);
                outputDiv.innerHTML += (data.message + '<br>');
            };

            chatSocket.onclose = function(e) {
                console.error('Chat socket closed unexpectedly');
            };

            chatSocket.onerror = function(e) {
                console.error('WebSocket error:', e);
            };
        }
    };

    sendMessageButton.onclick = function() {
        if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
            const message = messageInput.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInput.value = '';
        } else {
            console.error('WebSocket is not open.');
        }
    };
} else {
    console.error('Element with id="roomId" not found');
}
