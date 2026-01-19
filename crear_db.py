import sqlite3

def inicializar_db():
    conn = sqlite3.connect('especialidades_fae.db')
    cursor = conn.cursor()

    # Tabla de Alumnos (Basada en tu Excel de Antigüedades)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumnos (
            antiguedad INTEGER PRIMARY KEY,
            nombres TEXT NOT NULL
        )
    ''')

    # Tabla de BAT-7 (Aptitudes)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bat7 (
            alumno_antiguedad INTEGER,
            interes_1 TEXT,
            interes_2 TEXT,
            sugerencia_aptitudinal TEXT,
            FOREIGN KEY(alumno_antiguedad) REFERENCES alumnos(antiguedad)
        )
    ''')

    # Tabla de Preferencias (Afinidad)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preferencias (
            alumno_antiguedad INTEGER,
            opcion_1 TEXT,
            opcion_2 TEXT,
            opcion_descarte TEXT,
            FOREIGN KEY(alumno_antiguedad) REFERENCES alumnos(antiguedad)
        )
    ''')

    # Tabla de Cupos (68 cupos en total)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cupos (
            especialidad TEXT PRIMARY KEY,
            vacantes_iniciales INTEGER,
            vacantes_restantes INTEGER
        )
    ''')

    conn.commit()
    conn.close()
    print("Base de datos 'especialidades_fae.db' inicializada correctamente.")

if __name__ == "__main__":
    inicializar_db()