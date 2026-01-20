import sqlite3
import pandas as pd

DB = "especialidades_fae.db"

def obtener_estadisticas():
    conn = sqlite3.connect(DB)

    df = pd.read_sql("""
        SELECT 
            especialidad_asignada AS especialidad,
            COUNT(*) AS alumnos_asignados
        FROM resultados_finales
        GROUP BY especialidad_asignada
        ORDER BY alumnos_asignados DESC
    """, conn)

    cupos = pd.read_sql("""
        SELECT especialidad, vacantes_iniciales
        FROM cupos
    """, conn)

    conn.close()

    df = df.merge(cupos, on="especialidad", how="left")
    df["cupos_libres"] = df["vacantes_iniciales"] - df["alumnos_asignados"]

    return df
