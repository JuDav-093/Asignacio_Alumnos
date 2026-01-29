import sqlite3
import pandas as pd

DB = "especialidades_fae.db"

def obtener_estadisticas():
    conn = sqlite3.connect(DB)
    try:
        # 1. Obtener asignados
        df_res = pd.read_sql("""
            SELECT especialidad_asignada AS especialidad, COUNT(*) AS asignados 
            FROM resultados_finales 
            GROUP BY especialidad_asignada
        """, conn)
        
        # 2. Obtener cupos
        df_cupos = pd.read_sql("""
            SELECT nombre_especialidad AS especialidad, vacantes_iniciales 
            FROM especialidades
        """, conn)
    except Exception:
        # Si las tablas no existen aún (app recién desplegada)
        return pd.DataFrame(columns=["Especialidad", "Cupos Totales", "Alumnos Asignados", "Cupos Libres"])
    finally:
        conn.close()
    
    # 3. Procesar datos
    df = df_cupos.merge(df_res, on="especialidad", how="left").fillna(0)
    df["asignados"] = df["asignados"].astype(int)
    df["cupos_libres"] = df["vacantes_iniciales"] - df["asignados"]
    
    # IMPORTANTE: Definir nombres exactos para app.py
    df.columns = ["Especialidad", "Cupos Totales", "Alumnos Asignados", "Cupos Libres"]
    return df