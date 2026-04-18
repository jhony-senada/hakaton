from flask import Flask, render_template,session, request, send_file, jsonify,redirect,url_for# <-- Agrega send_file
from elevenlabs.client import ElevenLabs
# from elevenlabs.play import play <-- ¡Borra o comenta esta línea! Ya no la usaremos.
import os
import httpx
import io # <-- Agrega esto para manejar el archivo de audio en la memoria
import asyncio
import utilities.micro as micro
from utilities import base_de_datos as db

app = Flask(__name__)
app.secret_key ="super_secreto_uaq"
from utilities.webhook import webhook_bp

app = Flask(__name__)
app.register_blueprint(webhook_bp, url_prefix='/hooks')

http_client_inseguro = httpx.Client(verify=False)

client = ElevenLabs(
    api_key=os.getenv("ELEVEN_KEY"),
    httpx_client=http_client_inseguro 
)
#
# Rutas de interfaz (HTML)
# 

print("Version2")

@app.route('/')
def index():
    if 'matricula' in session:
        return redirect(url_for('main_menu'))
    return render_template('index.html')

@app.route('/menu')
def menu():
    if 'matricula' not in session:
        return redirect(url_for('index'))
    return render_template('mainMenu.html')

# 
# Rutas de API (Datos)
# 
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    expediente = data.get("expediente")
    password = data.get("password")

    # Consultar a la base de datos (Requiere que hayas añadido la columna password)
    query = "SELECT matricula, nombre FROM usuarios WHERE matricula = ? AND password = ?"
    usuario = db.ejecutar_query(query, (expediente, password))

    if usuario:
        session['matricula'] = usuario[0]['matricula'] # Guardar sesión en Flask
        return jsonify({"success": True, "matricula": usuario[0]['matricula']})
    else:
        return jsonify({"success": False, "error": "Expediente o contraseña incorrectos"}), 401

@app.route('/api/chat', methods=['POST'])
def chat_bot():
    data = request.get_json()
    mensaje_usuario = data.get("mensaje", "")
    
    # Toma la matrícula de la sesión de Flask, o del request si no existe
    matricula = session.get("matricula", data.get("matricula", "INVITADO"))
    sesion_activa = {"matricula": matricula}
    
    # Ejecutar Gemini
    respuesta = asyncio.run(micro.procesar_mensaje_usuario(sesion_activa, mensaje_usuario))
    return jsonify({"respuesta": respuesta})

@app.route('/recibir_mensaje', methods=['POST'])
def recibir():
    # Recibimos el texto que envía el JS (mensaje_ia)
    texto = request.form.get('mensaje_ia') 
    
    if not texto:
        return jsonify({"error": "No hay texto para leer"}), 400

    # Generar audio con ElevenLabs
    audio_generador = client.text_to_speech.convert(
        text=texto,
        voice_id="zl7szWVBXnpgrJmAalgz",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    audio_bytes = b"".join(audio_generador)
    
    return send_file(
        io.BytesIO(audio_bytes),
        mimetype="audio/mpeg"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)