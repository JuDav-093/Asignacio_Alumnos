import sqlite3
import pandas as pd

DB = "especialidades_fae.db"

def obtener_estadisticas():
    conn = sqlite3.connect(DB)
    
    # Obtener asignados
    df_res = pd.read_sql("""
        SELECT especialidad_asignada AS especialidad, COUNT(*) AS asignados 
        FROM resultados_finales 
        GROUP BY especialidad_asignada
    """, conn)
    
    # Obtener cupos base
    df_cupos = pd.read_sql("""
        SELECT nombre_especialidad AS especialidad, vacantes_iniciales 
        FROM especialidades
    """, conn)
    
    conn.close()
    
    # Unir y limpiar
    df = df_cupos.merge(df_res, on="especialidad", how="left").fillna(0)
    df["asignados"] = df["asignados"].astype(int)
    df["cupos_libres"] = df["vacantes_iniciales"] - df["asignados"]
    
    # RENOMBRADO EXPLÍCITO para evitar KeyError en app.py
    df.columns = ["Especialidad", "Cupos Totales", "Alumnos Asignados", "Cupos Libres"]
    
    return df