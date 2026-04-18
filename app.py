from flask import Flask, render_template, request, send_file # <-- Agrega send_file
from elevenlabs.client import ElevenLabs
# from elevenlabs.play import play <-- ¡Borra o comenta esta línea! Ya no la usaremos.
import os
import httpx
import io # <-- Agrega esto para manejar el archivo de audio en la memoria

app = Flask(__name__)

print("Version 2")

http_client_inseguro = httpx.Client(verify=False)

client = ElevenLabs(
    api_key=os.getenv("ELEVEN_KEY"),
    httpx_client=http_client_inseguro 
)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/saludo/<nombre>')
def saludar(nombre):
    return f"Hola {nombre}, bienvenido a mi API básica."

@app.route('/recibir_mensaje', methods=['POST'])
def recibir():
    texto = request.form.get('mensaje_usuario')
    
    print("--------------------------------------------------")
    print(f"NUEVO MENSAJE RECIBIDO: {texto}")
    print("--------------------------------------------------")

    # ElevenLabs genera el audio (nos devuelve un "generador" de pedacitos de audio)
    audio_generador = client.text_to_speech.convert(
        text=texto, # <-- TIP: ¡Puse la variable 'texto' aquí para que lea lo que escribes!
        voice_id="zl7szWVBXnpgrJmAalgz",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    # 1. Juntamos todos los pedacitos de audio en un solo bloque de datos (bytes)
    audio_bytes = b"".join(audio_generador)
    
    # 2. Le mandamos ese audio directamente al navegador del usuario
    return send_file(
        io.BytesIO(audio_bytes),
        mimetype="audio/mpeg"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)