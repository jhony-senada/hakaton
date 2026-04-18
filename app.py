import asyncio
from flask import Flask, request, jsonify, session
import micro  # Importamos tu lógica de Gemini

app = Flask(__name__)
app.secret_key = "super_secreto_uaq"

@app.route('/api/chat', methods=['POST'])
def chat_bot():
    data = request.get_json()
    mensaje_usuario = data.get("mensaje", "")

    if "matricula" not in session:
        session["matricula"] = data.get("matricula", "INVITADO")
    sesion_activa = {
        "matricula": session["matricula"]
    }
    respuesta = asyncio.run(micro.procesar_mensaje_usuario(sesion_activa, mensaje_usuario))
    return jsonify({"respuesta": respuesta})
