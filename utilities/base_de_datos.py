import sqlite3
from sqlite3 import Error

def dict_factory(cursor, row):
    """Convierte cada fila de la consulta en un diccionario limpio."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def ejecutar_query(query, parametros=None):
    """Se conecta a SQLite3, ejecuta el query y devuelve los datos."""
    conexion = None
    resultados = []
    
    try:
        # Aquí es donde ocurre la magia de SQLite3
        conexion = sqlite3.connect('UAQ_Datos.db')
        conexion.row_factory = dict_factory 
        cursor = conexion.cursor()
        
        if parametros:
            cursor.execute(query, parametros)
        else:
            cursor.execute(query)
            
        if query.strip().upper().startswith("SELECT"):
            resultados = cursor.fetchall()
        else:
            conexion.commit()
            
    except Error as e:
        print(f"Error de SQLite: {e}")
        
    finally:
        if conexion:
            conexion.close()
            
    return resultados