const sendMessageButton = document.querySelector('#sendMessage');
const messageInput = document.querySelector('#myInput');
const outputDiv = document.querySelector('#output');
const roomIdElement = document.querySelector('#roomId');
const currentUser = document.querySelector('#requestUser');

let chatSocket;

function openWebSocket() {
    if (roomIdElement) {
        const roomId = roomIdElement.textContent.trim();
        if (!chatSocket || chatSocket.readyState === WebSocket.CLOSED) {
            const wsUrl = `ws://${window.location.host}/ws/messanger/${roomId}/`;
            console.log('Connecting to WebSocket:', wsUrl);
            chatSocket = new WebSocket(wsUrl);

            chatSocket.onmessage = function(e) {
                const data = JSON.parse(e.data);
                console.log("Received data:", data);  

                const message = data.message || 'No message';
                const sender = data.sender || 'Unknown sender';
                const time = data.time || 'Unknown time';

                const senderClass = sender === currentUser.textContent.trim() ? 'sender' : 'receiver'; 
                if (message === 'No message') {
                    const formattedMessage = ``;
                    outputDiv.innerHTML += formattedMessage + '';
                } else {
                    const formattedMessage = `
                        <div class="message ${senderClass}">
                            <h5 class='author'>${sender}</h5> 
                            <p>${message}</p>
                            <small>[${time}]</small>
                        </div>
                    `;
                    outputDiv.innerHTML += formattedMessage + '<br>';
                }
            };

            chatSocket.onclose = function(e) {
                console.error('Chat socket closed unexpectedly');
            };

            chatSocket.onerror = function(e) {
                console.error('WebSocket error:', e);
            };
        }
    } else {
        console.error('Element with id="roomId" not found');
    }
}

// Automatically open WebSocket connection when the page loads
window.addEventListener('load', openWebSocket);

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
