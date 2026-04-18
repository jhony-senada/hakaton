import asyncio
import utilities.base_de_datos as db # ¡Aquí estamos conectando con tu archivo de SQLite3!
from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

async def procesar_mensaje_usuario(sesion_activa, mensaje_usuario):
    matricula = sesion_activa.get("matricula", "INVITADO") 
    
    # Usamos nuestro módulo db para hablar con SQLite3
    resultados_perfil = db.ejecutar_query(
        "SELECT rol, id_grupo FROM usuarios WHERE matricula = ?", 
        (matricula,)
    )
    
    if not resultados_perfil:
        rol_actual = 'invitado'
        grupo_actual = None
    else:
        perfil = resultados_perfil[0]
        rol_actual = perfil['rol']       
        grupo_actual = perfil['id_grupo'] 

    jerarquia_roles = ['invitado']
    if rol_actual == 'usuario':
        jerarquia_roles.append('usuario') 
    elif rol_actual == 'admin':
        jerarquia_roles.extend(['usuario', 'admin'])

    mensaje_lower = mensaje_usuario.lower()
    datos_recuperados = []

    if "trámite" in mensaje_lower or "inscripción" in mensaje_lower:
        placeholders = ', '.join(['?'] * len(jerarquia_roles)) 
        query_tramites = f"SELECT titulo, descripcion FROM tramites WHERE rol_requerido IN ({placeholders})"
        datos_recuperados = db.ejecutar_query(query_tramites, tuple(jerarquia_roles))
        
    elif "clase" in mensaje_lower or "horario" in mensaje_lower:
        if grupo_actual is None:
            datos_recuperados = "El usuario no tiene un grupo asignado para ver horarios."
        else:
            datos_recuperados = db.ejecutar_query(
                """SELECT c.materia, p.nombre, c.salon, c.hora_inicio 
                FROM clases_horarios c 
                JOIN profesores p ON c.id_profesor = p.id_profesor 
                WHERE id_grupo = ?""",
                (grupo_actual,)
            )

    prompt_final = f"""
    Eres un asistente escolar estricto y amable.
    Regla 1: Solo debes responder basándote en la información proporcionada abajo.
    Regla 2: Si la respuesta no está en la información, di 'No tengo acceso a esa información'.
    INFORMACIÓN RECUPERADA:
    {datos_recuperados}
    """
    
    respuesta_gemini = await enviar_a_gemini(prompt_final, mensaje_usuario)
    return respuesta_gemini

async def enviar_a_gemini(prompt_final, pregunta_del_alumno: str)->str:
    prompt = f"{prompt_final} PREGUNTA DEL USUARIO: {pregunta_del_alumno}"
    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash-lite-latest", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error al generar respuesta: {str(e)}"