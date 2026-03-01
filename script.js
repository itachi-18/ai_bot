const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const micBtn = document.getElementById('mic-btn');

async function sendMessage(text) {
    appendMessage('user', text);
    userInput.value = '';

    const response = await fetch('http://localhost:5005/webhooks/rest/webhook', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ sender: "user", message: text })
    });
    
    const data = await response.json();
    data.forEach(msg => {
        appendMessage('bot', msg.text);
        speakText(msg.text);
    });
}

function appendMessage(sender, text) {
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    div.innerText = text;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Speech to Text
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    micBtn.onclick = () => {
        recognition.start();
        document.getElementById('status').innerText = "● Listening...";
    };
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        sendMessage(transcript);
        document.getElementById('status').innerText = "● Online";
    };
}

// Text to Speech
function speakText(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utterance);
}

sendBtn.onclick = () => sendMessage(userInput.value);