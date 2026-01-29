import sqlite3
import pandas as pd

DB = "especialidades_fae.db"

def obtener_auditoria(antiguedad):
    conn = sqlite3.connect(DB)
    # Datos de entrada
    asp = pd.read_sql("SELECT * FROM aspirantes WHERE antiguedad=?", conn, params=(antiguedad,))
    # Resultado
    res = pd.read_sql("SELECT * FROM resultados_finales WHERE antiguedad=?", conn, params=(antiguedad,))
    # Detalle formateado
    det = pd.read_sql("SELECT detalle FROM auditoria_decisiones WHERE antiguedad=?", conn, params=(antiguedad,))
    conn.close()
    return asp, res, det