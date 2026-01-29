import pandas as pd
import sqlite3

DB = "especialidades_fae.db"

def cargar_desde_excel(file_ant, file_bat, file_afin):
    try:
        df_ant = pd.read_excel(file_ant)
        df_bat = pd.read_excel(file_bat, skiprows=1)
        df_af = pd.read_excel(file_afin, skiprows=1)

        # Limpieza de columnas
        for df in [df_ant, df_bat, df_af]:
            df.columns = df.columns.str.strip().str.lower()

        # Unir todos los datos por 'antiguedad'
        df_final = df_ant.merge(df_bat, on="antiguedad", how="left")
        df_final = df_final.merge(df_af, on="antiguedad", how="left", suffixes=('_bat', '_pref'))

        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM aspirantes")

        for _, r in df_final.iterrows():
            cursor.execute("""
                INSERT INTO aspirantes VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                int(r["antiguedad"]), r["nombres"].strip(),
                r["principal_bat"], r["optativa 1_bat"], r["sugerencia"],
                r["principal_pref"], r["optativa 1_pref"], r["descarte"]
            ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error en carga: {e}")
        return False