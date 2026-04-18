
##!usar este gemini-2.5-flash-lite-latest
import secrets
import asyncio
import base_de_datos as db ##!aca va la base de datos
from google import genai
client = genai.Client(api_key=secrets.key)

async def procesar_mensaje_usuario(sesion_activa, mensaje_usuario):
    matricula = sesion_activa.get("matricula", "INVITADO") 
    
    # 2. La base de datos devuelve una LISTA de diccionarios, no un diccionario directo
    resultados_perfil = db.ejecutar_query(
        "SELECT rol, id_grupo FROM usuarios WHERE matricula = %s", 
        (matricula,)
    )
    
    # 3. Validación de seguridad: ¿Qué pasa si la matrícula no existe en la BD?
    if not resultados_perfil:
        rol_actual = 'invitado'
        grupo_actual = None
    else:
        perfil = resultados_perfil[0]     # Extraemos el primer diccionario de la lista
        rol_actual = perfil['rol']       
        grupo_actual = perfil['id_grupo'] 

    jerarquia_roles = ['invitado']
    if rol_actual == 'usuario':
        jerarquia_roles.append('usuario') # append en lugar de extend para un solo item
    elif rol_actual == 'admin':
        jerarquia_roles.extend(['usuario', 'admin'])

    mensaje_lower = mensaje_usuario.lower()
    datos_recuperados = []

    if "trámite" in mensaje_lower or "inscripción" in mensaje_lower:
        # 4. Ajuste para que el 'WHERE IN' funcione bien en el conector de MySQL
        placeholders = ', '.join(['%s'] * len(jerarquia_roles)) 
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
                WHERE id_grupo = %s""",
                (grupo_actual,)
            )

    prompt_final = f"""
    Eres un asistente escolar estricto y amable.
    Regla 1: Solo debes responder basándote en la información proporcionada abajo.
    Regla 2: Si la respuesta no está en la información, di 'No tengo acceso a esa información'.
    INFORMACIÓN RECUPERADA:
    {datos_recuperados}
    """
    
    # 5. Agregamos el 'await' porque estamos llamando a una función asíncrona
    respuesta_gemini = await enviar_a_gemini(prompt_final, mensaje_usuario)
    
    return respuesta_gemini

async def enviar_a_gemini(prompt_final, pregunta_del_alumno: str)->str:
    """Toma el contexto de la base de datos y la pregunta del alumno 
    para generar una respuesta asíncrona con Gemini."""
    prompt = f"""
    {prompt_final} PREGUNTA DEL USUARIO: {pregunta_del_alumno}
    """
    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error al generar respuesta: {str(e)}"

# --- Ejemplo de cómo correrlo para probar ---
if __name__ == "__main__":
    # Como todo el flujo es asíncrono, necesitamos iniciarlo con asyncio
    async def probar_chat():
        sesion_simulada = {"matricula": "UAQ-345678"} 
        pregunta = "¿A qué hora tengo clase hoy y en qué salón?"
        
        print(f"Pregunta: {pregunta}")
        respuesta = await procesar_mensaje_usuario(sesion_simulada, pregunta)
        print(f"Respuesta IA:\n{respuesta}")

    asyncio.run(probar_chat())