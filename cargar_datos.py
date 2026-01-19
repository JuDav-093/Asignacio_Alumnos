import pandas as pd
import sqlite3

def limpiar_columnas(df):
    # Convierte encabezados a mayúsculas y quita espacios en blanco
    df.columns = [str(c).strip().upper() for c in df.columns]
    return df

def cargar_todo():
    conn = sqlite3.connect('especialidades_fae.db')
    
    try:
        # 1. CARGAR ANTIGÜEDADES
        # Si el Excel tiene celdas vacías arriba, pandas podría no detectar los nombres.
        # Intentamos leerlo directamente.
        df_ant = pd.read_excel('antiguedades_alumnos.xlsx')
        df_ant = limpiar_columnas(df_ant)
        
        for _, row in df_ant.iterrows():
            # Usamos get() para evitar que el programa se cierre si no encuentra la columna exacta
            ant = row.get('ANTIGUEDAD') or row.get('ORD') or row.get('ORDEN')
            nombre = row.get('NOMBRES') or row.get('NOMBRE Y APELLIDO')
            
            if pd.notna(ant):
                conn.execute("INSERT INTO alumnos (antiguedad, nombres) VALUES (?, ?)", 
                             (int(ant), str(nombre)))
        print("✔ Antigüedades cargadas correctamente.")

        # 2. CARGAR BAT-7 (Ajustado a la estructura de tus archivos)
        # Skiprows=3 porque en tus archivos la data real empieza en la fila 4 
        df_bat = pd.read_excel('BAT_7.xlsx', skiprows=3)
        df_bat = limpiar_columnas(df_bat)
        
        for _, row in df_bat.iterrows():
            ant = row.get('ORD')
            if pd.notna(ant):
                conn.execute("INSERT INTO bat7 VALUES (?, ?, ?, ?)", 
                             (int(ant), str(row.get('PRINCIPAL')), 
                              str(row.get('OPTATIVA 1')), 
                              str(row.get('SUGERENCIA SEGÚN ESTUDIO'))))
        print("✔ Datos BAT-7 cargados.")

        # 3. CARGAR AFINIDAD DEL ALUMNO
        df_af = pd.read_excel('AFINIDAD_ALUMNO.xlsx', skiprows=3)
        df_af = limpiar_columnas(df_af)
        
        for _, row in df_af.iterrows():
            ant = row.get('ORD')
            if pd.notna(ant):
                conn.execute("INSERT INTO preferencias VALUES (?, ?, ?, ?)", 
                             (int(ant), str(row.get('PRINCIPAL')), 
                              str(row.get('OPTATIVA 1')), 
                              str(row.get('DESCARTE'))))
        print("✔ Preferencias cargadas.")

        conn.commit()
    except Exception as e:
        print(f"❌ Error durante la carga: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    cargar_todo()