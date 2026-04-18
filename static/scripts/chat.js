// Seleccionamos todos los elementos necesarios
const chatWidget = document.getElementById('aiChatWidget');
const chatHeader = document.getElementById('chatHeader');
const chatResizer = document.getElementById('chatResizer');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const messages = document.getElementById('messages');

// Nuevos elementos de audio
const ttsToggleBtn = document.getElementById('ttsToggleBtn');
const ttsIconOff = document.getElementById('ttsIconOff');
const ttsIconOn = document.getElementById('ttsIconOn');
const micBtn = document.getElementById('micBtn');

// ==========================================
// 1. LÓGICA PARA REDIMENSIONAR (RESIZER)
// ==========================================
let isResizing = false;

chatResizer.addEventListener('mousedown', (e) => {
    isResizing = true;
    e.preventDefault();
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', stopResizing);
    document.body.style.cursor = 'nwse-resize';
});

function handleMouseMove(e) {
    if (!isResizing) return;
    const newWidth = window.innerWidth - e.clientX - 20; 
    const newHeight = window.innerHeight - e.clientY;

    if (newWidth > 280) chatWidget.style.width = `${newWidth}px`;
    if (newHeight > 100) chatWidget.style.height = `${newHeight}px`;
}

function stopResizing() {
    isResizing = false;
    document.removeEventListener('mousemove', handleMouseMove);
    document.body.style.cursor = 'default';
}

// ==========================================
// 2. LÓGICA DE COLAPSO / EXPANSIÓN
// ==========================================
chatHeader.addEventListener('click', () => {
    const isOpen = chatWidget.classList.toggle('open');
    if (!isOpen) {
        chatWidget.style.height = '40px';
    } else {
        if (chatWidget.style.height === '40px' || !chatWidget.style.height) {
            chatWidget.style.height = '500px';
        }
        if (messages.childElementCount === 0) {
            const saludo = 'Hola! Soy tu asesor AI, estoy listo para ayudarte. ¿En qué puedo orientarte hoy?';
            addMessage('ai', saludo);
            playElevenLabsAudio(saludo);
        }
    }
});

// ==========================================
// 3. TEXT-TO-SPEECH (ELEVENLABS PLACEHOLDER)
// ==========================================
let isTtsEnabled = false;
let currentAudio = null;//Para controlar el audio actual y detenerlo si se desactiva el TTS

ttsToggleBtn.addEventListener('click', () => {
    isTtsEnabled = !isTtsEnabled;
    if (isTtsEnabled) {
        ttsIconOff.style.display = 'none';
        ttsIconOn.style.display = 'block';
        const mensajesIA = document.querySelectorAll('.ai-message');
        if (mensajesIA.length > 0) {
            const ultimoMensaje = mensajesIA[mensajesIA.length - 1].innerText;
            playElevenLabsAudio(ultimoMensaje);
        }
    } else {
        // Cambiar icono a "Apagado"
        ttsIconOff.style.display = 'block';
        ttsIconOn.style.display = 'none';
        
        // Detener el audio inmediatamente si el usuario apaga el botón
        if (currentAudio) {
            currentAudio.pause();
            currentAudio.currentTime = 0;
        }
    }
});
function playElevenLabsAudio(text) {
    if (!isTtsEnabled) return;
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
    }
    const formData = new FormData();
    formData.append('mensaje_ia', text);
    fetch(fetch('/recibir_mensaje', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) throw new Error("Error en la respuesta del servidor");
        return response.blob();
    })
    .then(audioBlob => {
        // 3. Creamos la URL temporal y reproducimos el audio
        const audioUrl = URL.createObjectURL(audioBlob);
        currentAudio = new Audio(audioUrl); 
        currentAudio.play();
    })
    .catch(error => {
        console.error("Error de conexión al reproducir audio:", error);
    }));
}

// ==========================================
// 4. SPEECH-TO-TEXT (MICRÓFONO)
// ==========================================
// Verificamos soporte en el navegador
let mediaRecorder;
let audioChunks = [];
let isRecording = false;

// Asegúrate de tener las referencias a tus elementos
// const micBtn = document.getElementById('micBtn');
// const userInput = document.getElementById('userInput');

micBtn.addEventListener('click', async () => {
    if (isRecording) {
        // 1. Si está grabando, detenemos la grabación
        mediaRecorder.stop();
        isRecording = false;
        micBtn.classList.remove('recording');
        userInput.placeholder = "Procesando audio..."; // Mensaje mientras el servidor responde
        
    } else {
        // 2. Si no está grabando, pedimos permiso e iniciamos
        try {
            // Pedimos acceso al micrófono
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = []; // Limpiamos grabaciones anteriores
            userInput.value = '';

            // 3. Mientras el usuario habla, vamos guardando los "pedacitos" de audio
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };

            // 4. Cuando el usuario detiene la grabación (al presionar el botón de nuevo)
            mediaRecorder.onstop = async () => {
                // Creamos un archivo "Blob" con todo el audio capturado
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' }); 
                
                // Preparamos los datos para enviarlos al servidor (como si fuera un formulario web)
                const formData = new FormData();
                formData.append('audio', audioBlob, 'grabacion.webm');

                try {
                    /* ========================================================
                       🔴 ENVÍO AL BACKEND 🔴
                    ======================================================== */
                    // Cambia '/api/transcribe' por la URL real de tu servidor Flask/Node
                    const response = await fetch('/api/transcribe', {
                        method: 'POST',
                        body: formData
                    });

                    if (!response.ok) throw new Error("Error en el servidor");

                    const data = await response.json();
                    
                    // Asumiendo que tu backend te devuelve el texto así: { "text": "Hola, ¿cómo estás?" }
                    if (data.text) {
                        userInput.value = data.text;
                        userInput.placeholder = "Escribe o habla tu mensaje...";
                        
                        // Si quieres que se envíe al chat automáticamente:
                        // sendMessage(); 
                    }

                } catch (error) {
                    console.error("Error al enviar el audio al servidor:", error);
                    userInput.placeholder = "Error al procesar el audio. Intenta escribir.";
                } finally {
                    // Apagamos el micrófono para que no se quede la luz roja encendida en el navegador
                    stream.getTracks().forEach(track => track.stop());
                }
            };

            // Arrancamos la grabación
            mediaRecorder.start();
            isRecording = true;
            micBtn.classList.add('recording');
            userInput.placeholder = "Escuchando...";

        } catch (err) {
            console.error("Error al acceder al micrófono:", err);
            userInput.placeholder = "Permiso de micrófono denegado.";
        }
    }
});

// ==========================================
// 5. LÓGICA DE MENSAJERÍA
// ==========================================
function addMessage(sender, text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = sender === 'user' ? 'user-message' : 'ai-message';
    messageDiv.innerText = text;
    messages.appendChild(messageDiv);
    messages.scrollTop = messages.scrollHeight; 
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (text === "") return;
    
    // Si estaba grabando, detenemos el micro
    if (isRecording) recognition.stop();

    addMessage('user', text);
    userInput.value = '';
    const matricula = localStorage.getItem('matricula') || "INVITADO"; // Reemplaza con la matrícula real del usuario

// Opcional: Podrías añadir un indicador de "Escribiendo..." aquí

    try {
        // 2. Enviar el mensaje a tu backend en Flask
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mensaje: text , matricula: matricula})
        });
        if (!response.ok) throw new Error("Error en la respuesta del servidor");

        const data = await response.json();
        const respuestaIA = data.respuesta;

        // 3. Mostrar la respuesta de Gemini en el chat
        addMessage('ai', respuestaIA);
        // 4. Reproducir el audio (TTS)
        playElevenLabsAudio(respuestaIA);

    } catch (error) {
        console.error("Error comunicándose con el Asesor AI:", error);
        addMessage('ai', "Lo siento, perdí la conexión con los servidores de la universidad. Intenta de nuevo.");
    }
}

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') sendMessage();
});