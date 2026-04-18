const chatWidget = document.getElementById('aiChatWidget');
const chatResizer = document.getElementById('chatResizer');

// --- LÓGICA PARA REDIMENSIONAR ---
let isResizing = false;

chatResizer.addEventListener('mousedown', (e) => {
    isResizing = true;
    e.preventDefault();
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', stopResizing);
    // Añadimos una clase para evitar selecciones de texto mientras arrastramos
    document.body.style.cursor = 'nwse-resize';
});

function handleMouseMove(e) {
    if (!isResizing) return;

    // Calculamos el nuevo ancho y alto basado en la posición del mouse
    // Como el widget está pegado a la derecha y abajo (bottom:0, right:20)
    const newWidth = window.innerWidth - e.clientX - 20; 
    const newHeight = window.innerHeight - e.clientY;

    if (newWidth > 280) {
        chatWidget.style.width = `${newWidth}px`;
    }
    if (newHeight > 100) {
        chatWidget.style.height = `${newHeight}px`;
    }
}

function stopResizing() {
    isResizing = false;
    document.removeEventListener('mousemove', handleMouseMove);
    document.body.style.cursor = 'default';
}

// --- MODIFICACIÓN EN LA LÓGICA DE COLAPSO ---
chatHeader.addEventListener('click', () => {
    const isOpen = chatWidget.classList.toggle('open');
    
    if (!isOpen) {
        // Al cerrar, reseteamos a la altura de la cabecera
        chatWidget.style.height = '40px';
    } else {
        // Al abrir, si no tiene un tamaño manual previo, ponemos el default
        if (chatWidget.style.height === '40px' || !chatWidget.style.height) {
            chatWidget.style.height = '500px';
        }
    }
});