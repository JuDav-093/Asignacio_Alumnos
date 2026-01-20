import sqlite3
import pandas as pd

DB = "especialidades_fae.db"

def validar_datos():
    conn = sqlite3.connect(DB)

    alumnos = pd.read_sql("SELECT antiguedad FROM alumnos", conn)
    bat = pd.read_sql("SELECT alumno_antiguedad FROM bat7", conn)
    pref = pd.read_sql("SELECT alumno_antiguedad FROM preferencias", conn)

    conn.close()

    errores = []

    set_alumnos = set(alumnos["antiguedad"])
    set_bat = set(bat["alumno_antiguedad"])
    set_pref = set(pref["alumno_antiguedad"])

    if set_alumnos != set_bat:
        errores.append("❌ BAT-7 no coincide con antigüedades")

    if set_alumnos != set_pref:
        errores.append("❌ Afinidad no coincide con antigüedades")

    duplicados = alumnos["antiguedad"].duplicated().sum()
    if duplicados > 0:
        errores.append(f"❌ Hay {duplicados} antigüedades duplicadas")

    if errores:
        return False, errores

    return True, ["✔ Validación completa: datos consistentes"]
