import sqlite3
import pandas as pd

DB = "especialidades_fae.db"

def obtener_auditoria(antiguedad):
    conn = sqlite3.connect(DB)

    alumno = pd.read_sql(
        "SELECT * FROM alumnos WHERE antiguedad=?",
        conn, params=(antiguedad,)
    )

    bat = pd.read_sql(
        "SELECT * FROM bat7 WHERE alumno_antiguedad=?",
        conn, params=(antiguedad,)
    )

    pref = pd.read_sql(
        "SELECT * FROM preferencias WHERE alumno_antiguedad=?",
        conn, params=(antiguedad,)
    )

    res = pd.read_sql(
        "SELECT * FROM resultados_finales WHERE antiguedad=?",
        conn, params=(antiguedad,)
    )

    conn.close()

    return alumno, bat, pref, res
