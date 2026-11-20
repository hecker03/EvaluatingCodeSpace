document.addEventListener('DOMContentLoaded', function() {
    const chatWidget = document.createElement('div');
    chatWidget.className = 'chat-widget-container';
    chatWidget.innerHTML = `
        <div class="chat-window" id="chatWindow">
            <div class="chat-header">
                <h3>AI Assistant</h3>
                <button class="close-chat-btn" id="closeChat">×</button>
            </div>
            <div class="chat-messages" id="chatMessages">
                <div class="message bot">Hello! How can I help you today?</div>
            </div>
            <div class="typing-indicator" id="typingIndicator">AI is typing...</div>
            <div class="chat-input-area">
                <input type="text" id="chatInput" placeholder="Type a message...">
                <button class="send-btn" id="sendMessage">➤</button>
            </div>
        </div>
        <button class="chat-toggle-btn" id="toggleChat">💬</button>
    `;
    document.body.appendChild(chatWidget);

    const toggleBtn = document.getElementById('toggleChat');
    const closeBtn = document.getElementById('closeChat');
    const chatWindow = document.getElementById('chatWindow');
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendMessage');
    const messagesContainer = document.getElementById('chatMessages');
    const typingIndicator = document.getElementById('typingIndicator');

    function toggleChat() {
        chatWindow.classList.toggle('open');
        if (chatWindow.classList.contains('open')) {
            chatInput.focus();
        }
    }

    toggleBtn.addEventListener('click', toggleChat);
    closeBtn.addEventListener('click', toggleChat);

    function addMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        msgDiv.textContent = text;
        messagesContainer.appendChild(msgDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        addMessage(message, 'user');
        chatInput.value = '';
        typingIndicator.style.display = 'block';

        try {
            const response = await fetch('/chat/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken() // Assuming you have a way to get CSRF token
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            typingIndicator.style.display = 'none';
            
            if (data.error) {
                addMessage('Error: ' + data.error, 'bot');
            } else {
                addMessage(data.response, 'bot');
            }
        } catch (error) {
            typingIndicator.style.display = 'none';
            addMessage('Error: Could not connect to server.', 'bot');
            console.error('Error:', error);
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Helper to get CSRF token from meta tag or cookie
    function getCsrfToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? meta.getAttribute('content') : '';
    }
});
