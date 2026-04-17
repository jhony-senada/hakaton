# 1. IMPORTANTE: Agrega 'request' a esta línea
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/saludo/<nombre>')
def saludar(nombre):
    return f"Hola {nombre}, bienvenido a mi API básica."

# 2. NUEVA RUTA PARA RECIBIR EL POST
@app.route('/recibir_mensaje', methods=['POST'])
def recibir():
    # Extraemos el texto usando el 'name' que pusimos en el input del HTML
    texto = request.form.get('mensaje_usuario')
    
    # 3. Lo imprimimos en la consola donde estás ejecutando el servidor
    print("--------------------------------------------------")
    print(f"NUEVO MENSAJE RECIBIDO: {texto}")
    print("--------------------------------------------------")
    
    # El servidor siempre debe devolver una respuesta al navegador
    return "¡Mensaje recibido e impreso en la consola!"

if __name__ == '__main__':
    app.run(port=5000, debug=True)