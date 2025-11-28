// Agent avatar SVG definitions
const avatarSVGs = {
    alex: `<object data="avatars/alex.svg" type="image/svg+xml" class="avatar-svg"></object>`,
    maya: `<object data="avatars/maya.svg" type="image/svg+xml" class="avatar-svg"></object>`,
    jordan: `<object data="avatars/jordan.svg" type="image/svg+xml" class="avatar-svg"></object>`,
    dr_chen: `<object data="avatars/dr_chen.svg" type="image/svg+xml" class="avatar-svg"></object>`,
    sam: `<object data="avatars/sam.svg" type="image/svg+xml" class="avatar-svg"></object>`,
    river: `<object data="avatars/river.svg" type="image/svg+xml" class="avatar-svg"></object>`
};

// Configuration
const BASE_URL = 'localhost:8000';

// REST
const API_URL = `http://${BASE_URL}`;

// WebSocket
const WS_URL = `ws://${BASE_URL}`;

const USER_ID = 'demo_user_' + Date.now();

let currentEmotion = 'calm';
let currentRole = 'Individual';
let ws = null;
let currentAge = 25;
let isTalking = false;

// Agent info
const agentInfo = {
    alex: { name: 'Alex', role: 'Young Adult Peer', color: '#3498db' },
    maya: { name: 'Maya', role: 'Therapist', color: '#e74c3c' },
    jordan: { name: 'Jordan', role: 'Teen Peer', color: '#9b59b6' },
    dr_chen: { name: 'Dr. Chen', role: 'Activities Specialist', color: '#f39c12' },
    sam: { name: 'Sam', role: 'Parent Peer', color: '#1abc9c' },
    river: { name: 'River', role: 'Sibling Peer', color: '#34495e' }
};

// DOM elements
const avatarDisplay = document.getElementById('avatarDisplay');
const agentNameLarge = document.getElementById('agentNameLarge');
const agentRoleLarge = document.getElementById('agentRoleLarge');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const chatArea = document.getElementById('chatArea');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const emotionButtons = document.querySelectorAll('.emotion-btn');
const roleButtons = document.querySelectorAll('.agent-avatar');
const ageInput = document.getElementById('ageInput');

// Initialize with default avatar
setAvatar('default');

function setAvatar(agent) {
    currentAgent = agent;

    if (agent === 'thinking...' || agent === 'thinking___') return;

    if (agent === 'default' || agent === 'crisis_mcp' || agent === 'crisis_fallback') {
        avatarDisplay.innerHTML = `
                    <svg viewBox="0 0 200 200" class="avatar-svg">
                        <circle cx="100" cy="100" r="80" fill="url(#defaultGradient)"/>
                        <defs>
                            <linearGradient id="defaultGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                                <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                            </linearGradient>
                        </defs>
                        <circle cx="100" cy="100" r="80" fill="url(#defaultGradient)"/>
                        <text x="100" y="110" text-anchor="middle" font-size="60" fill="white">🤝</text>
                    </svg>
                `;
        agentNameLarge.textContent = 'SpectrumCircle';
        agentRoleLarge.textContent = 'Your Support Community';
    } else {
        avatarDisplay.innerHTML = avatarSVGs[agent] || avatarSVGs['alex'];
        const info = agentInfo[agent];
        agentNameLarge.textContent = info.name;
        agentRoleLarge.textContent = info.role;
    }
}

function startTalking() {
    isTalking = true;
    avatarDisplay.classList.add('talking');
    statusDot.classList.add('active');
    statusText.textContent = 'Speaking...';
}

function stopTalking() {
    isTalking = false;
    avatarDisplay.classList.remove('talking');
    statusDot.classList.remove('active');
    statusText.textContent = 'Listening';
}

function startThinking() {
    avatarDisplay.classList.add('thinking');
    statusText.textContent = 'Thinking...';
}

function stopThinking() {
    avatarDisplay.classList.remove('thinking');
}

// Create a default profile
async function init() {
    try {
        const response = await fetch(`${API_URL}/profiles`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: USER_ID,
                age: 25,
                communication_preference: 'direct',
                sensory_profile: {
                    seeking: ['proprioceptive'],
                    avoiding: ['auditory']
                }
            })
        });
    } catch (error) {
        console.error('Profile might already exist');
    }

    connectWebSocket();
}

// Connect to WebSocket
function connectWebSocket() {
    ws = new WebSocket(`${WS_URL}/ws/chat/${USER_ID}`);

    ws.onopen = () => {
        sendButton.disabled = false;
        statusText.textContent = 'Ready to help';
    };

    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            handleWebSocketMessage(data);
        } catch (error) {
            console.error('Error parsing WebSocket message:', error);
        }
    };

    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        addSystemMessage('Connection error. Please refresh the page.');
        statusText.textContent = 'Connection error';
    };

    ws.onclose = () => {
        sendButton.disabled = true;
        statusText.textContent = 'Disconnected';
    };
}

function convertAgent(agent) {
    return agent.toLowerCase().replaceAll(' ', '').replaceAll('.', '_');
}

// Handle WebSocket messages
function handleWebSocketMessage(data) {
    if (data.type === 'system') {
        addSystemMessage(data.message);
    } else if (data.type === 'typing') {
        showTypingIndicator();
        setAvatar(convertAgent(data.agent));
        startThinking();
    } else if (data.type === 'message') {
        hideTypingIndicator();
        stopThinking();
        setAvatar(convertAgent(data.agent));
        addAgentMessage(data.agent, data.message, data.is_crisis);

        startTalking();
        const messageLength = data.message.length;
        const talkDuration = Math.min(messageLength * 30, 5000); // Max 5 seconds
        setTimeout(stopTalking, talkDuration);
    } else if (data.type === 'error') {
        addSystemMessage('Error: ' + data.message);
        stopThinking();
        stopTalking();
    }
}

function sendMessage() {
    const message = messageInput.value.trim();

    if (!message || !ws || ws.readyState !== WebSocket.OPEN) {
        return;
    }

    addUserMessage(message);

    ws.send(JSON.stringify({
        message: message,
        emotional_state: currentEmotion,
        age: currentAge,
        rol: currentRole
    }));

    messageInput.value = '';
    setAvatar('default');
}

function addUserMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';
    messageDiv.innerHTML = `
                <div class="message-bubble">${escapeHtml(text)}</div>
            `;
    chatArea.appendChild(messageDiv);
    scrollToBottom();
}

function addAgentMessage(agent, text, isCrisis = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message agent';

    messageDiv.innerHTML = `
                <div class="message-bubble ${isCrisis ? 'crisis' : ''}">${formatMessage(text)}</div>
            `;

    chatArea.appendChild(messageDiv);
    scrollToBottom();
}

function addSystemMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'system-message';
    messageDiv.textContent = text;
    chatArea.appendChild(messageDiv);
    scrollToBottom();
}

function showTypingIndicator() {
    hideTypingIndicator();

    const indicator = document.createElement('div');
    indicator.id = 'typingIndicator';
    indicator.className = 'message agent';
    indicator.innerHTML = `
                <div class="typing-indicator">
                    <div class="typing-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            `;
    chatArea.appendChild(indicator);
    scrollToBottom();
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

function formatMessage(text) {
    text = escapeHtml(text);

    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');

    text = text.replace(/\n/g, '<br>');

    text = text.replace(/^- /gm, '• ');

    return text;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function scrollToBottom() {
    chatArea.scrollTop = chatArea.scrollHeight;
}

// Event listeners
sendButton.addEventListener('click', sendMessage);

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

emotionButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        emotionButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentEmotion = btn.dataset.emotion;
    });
});

roleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        roleButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentRole = btn.dataset.role;
    });
});

ageInput.addEventListener('change', (e) => {
    currentAge = e.target.value;
});

init();