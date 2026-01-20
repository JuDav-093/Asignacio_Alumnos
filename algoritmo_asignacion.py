import sqlite3
import pandas as pd
import unicodedata
import streamlit as st

DB = "especialidades_fae.db"

def norm(txt):
    if not txt or pd.isna(txt):
        return ""
    t = unicodedata.normalize("NFKD", str(txt))
    t = "".join(c for c in t if not unicodedata.combining(c))
    return t.upper().strip()

def ejecutar_asignacion():
    conn = sqlite3.connect(DB)

    alumnos = pd.read_sql(
        "SELECT * FROM alumnos ORDER BY antiguedad ASC", conn
    )

    cupos = pd.read_sql("SELECT * FROM cupos", conn)
    cupos["norm"] = cupos["especialidad"].apply(norm)
    cupos.set_index("norm", inplace=True)

    resultados = []

    for _, a in alumnos.iterrows():
        ant = a["antiguedad"]
        nombre = a["nombres"]

        bat = pd.read_sql(
            "SELECT * FROM bat7 WHERE alumno_antiguedad=?",
            conn, params=(ant,)
        ).iloc[0]

        pref = pd.read_sql(
            "SELECT * FROM preferencias WHERE alumno_antiguedad=?",
            conn, params=(ant,)
        ).iloc[0]

        opciones = [
            (norm(pref["opcion_1"]), "Preferencia principal"),
            (norm(pref["opcion_2"]), "Preferencia secundaria"),
            (norm(bat["sugerencia_aptitudinal"]), "Sugerencia BAT-7")
        ]

        asignada = None
        motivo = None

        for opt, causa in opciones:
            if opt in cupos.index and cupos.at[opt, "vacantes_restantes"] > 0:
                asignada = cupos.at[opt, "especialidad"]
                cupos.at[opt, "vacantes_restantes"] -= 1
                motivo = causa
                break

        # 🔴 ASIGNACIÓN FORZADA (si no hubo cupo en nada)
        if not asignada:
            for idx, row in cupos.iterrows():
                if row["vacantes_restantes"] > 0:
                    asignada = row["especialidad"]
                    cupos.at[idx, "vacantes_restantes"] -= 1
                    motivo = "Asignación administrativa por disponibilidad"
                    break

        resultados.append({
            "antiguedad": ant,
            "nombres": nombre,
            "especialidad_asignada": asignada,
            "motivo_asignacion": motivo
        })

    df = pd.DataFrame(resultados)
    df.to_sql("resultados_finales", conn, if_exists="replace", index=False)

    cupos.reset_index(drop=True).to_sql(
        "cupos", conn, if_exists="replace", index=False
    )

    conn.commit()
    conn.close()
    return True
