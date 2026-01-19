import sqlite3
import pandas as pd

def obtener_jerarquia_alumno(bat7, pref):
    """
    Lógica de Jerarquización: Define las 3 opciones principales basadas 
    en el cruce de aptitud y deseo del alumno.
    """
    opciones = []
    # Prioridad 1: Sugerencia del BAT-7 cruzada con su Opción 1 [cite: 160, 387, 404]
    opciones.append(pref['opcion_1']) 
    # Prioridad 2: Interés Ocupacional 1 del BAT-7 o su Opción 2 [cite: 160, 390]
    opciones.append(pref['opcion_2'])
    # Prioridad 3: Segunda sugerencia del BAT-7 o perfil de seguridad (Descarte) [cite: 160]
    opciones.append(bat7['sugerencia_aptitudinal'])
    
    return opciones

def ejecutar_asignacion():
    conn = sqlite3.connect('especialidades_fae.db')
    
    # 1. Cargar alumnos ordenados por ANTIGÜEDAD (Mérito) [cite: 132, 405]
    alumnos = pd.read_sql_query("SELECT * FROM alumnos ORDER BY antiguedad ASC", conn)
    
    # 2. Cargar cupos actuales
    cupos = pd.read_sql_query("SELECT * FROM cupos", conn).set_index('especialidad')
    
    resultados = []

    for index, alumno in alumnos.iterrows():
        ant = alumno['antiguedad']
        
        # Obtener datos de BAT-7 y Preferencias para este alumno
        bat = pd.read_sql_query(f"SELECT * FROM bat7 WHERE alumno_antiguedad = {ant}", conn).iloc[0]
        pref = pd.read_sql_query(f"SELECT * FROM preferencias WHERE alumno_antiguedad = {ant}", conn).iloc[0]
        
        # Generar sus 3 opciones jerárquicas
        opciones_jerarquicas = obtener_jerarquia_alumno(bat, pref)
        
        asignada = "SIN ASIGNAR"
        alternativa = "PENDIENTE"
        
        # Lógica de Asignación: Buscar cupo en orden jerárquico [cite: 131, 140, 405]
        for i, opcion in enumerate(opciones_jerarquicas):
            if opcion in cupos.index and cupos.at[opcion, 'vacantes_restantes'] > 0:
                asignada = opcion
                # Descontar cupo
                cupos.at[opcion, 'vacantes_restantes'] -= 1
                # Definir la alternativa (la siguiente opción que hubiera tenido)
                alternativa = opciones_jerarquicas[i+1] if i+1 < len(opciones_jerarquicas) else "N/A"
                break
        
        resultados.append({
            'antiguedad': ant,
            'nombres': alumno['nombres'],
            'especialidad_asignada': asignada,
            'especialidad_alternativa': alternativa
        })

    # Guardar resultados en una nueva tabla
    df_final = pd.DataFrame(resultados)
    df_final.to_sql('resultados_finales', conn, if_exists='replace', index=False)
    
    # Actualizar cupos en la DB
    cupos.reset_index().to_sql('cupos', conn, if_exists='replace', index=False)
    
    conn.close()
    print("Proceso de asignación completado exitosamente.")
    return df_final

if __name__ == "__main__":
    ejecutar_asignacion()