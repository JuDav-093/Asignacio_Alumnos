import pandas as pd
import sqlite3

DB = "especialidades_fae.db"

def cargar_desde_excel(file_ant, file_bat, file_afin):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM alumnos")
        cursor.execute("DELETE FROM bat7")
        cursor.execute("DELETE FROM preferencias")

        # ===== ANTIGÜEDADES =====
        df_ant = pd.read_excel(file_ant)
        df_ant.columns = df_ant.columns.str.strip().str.lower()

        for _, r in df_ant.iterrows():
            cursor.execute(
                "INSERT INTO alumnos VALUES (?, ?)",
                (int(r["antiguedad"]), r["nombres"].strip())
            )

        # ===== BAT-7 =====
        df_bat = pd.read_excel(file_bat, skiprows=1)
        df_bat.columns = df_bat.columns.str.strip().str.lower()

        for _, r in df_bat.iterrows():
            cursor.execute(
                "INSERT INTO bat7 VALUES (?, ?, ?, ?)",
                (
                    int(r["antiguedad"]),
                    r["principal"],
                    r["optativa 1"],
                    r["sugerencia"]
                )
            )

        # ===== AFINIDAD =====
        df_af = pd.read_excel(file_afin, skiprows=1)
        df_af.columns = df_af.columns.str.strip().str.lower()

        for _, r in df_af.iterrows():
            cursor.execute(
                "INSERT INTO preferencias VALUES (?, ?, ?, ?)",
                (
                    int(r["antiguedad"]),
                    r["principal"],
                    r["optativa 1"],
                    r["descarte"]
                )
            )

        conn.commit()
        return True

    except Exception as e:
        print(e)
        return False

    finally:
        conn.close()
