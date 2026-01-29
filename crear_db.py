import sqlite3

DB = "especialidades_fae.db"

def inicializar_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Tabla de Aspirantes (Entrada)
    cursor.execute("DROP TABLE IF EXISTS aspirantes")
    cursor.execute("""
    CREATE TABLE aspirantes (
        antiguedad INTEGER PRIMARY KEY,
        nombres TEXT,
        bat_principal TEXT,
        bat_optativa TEXT,
        bat_sugerencia TEXT,
        pref_principal TEXT,
        pref_optativa TEXT,
        pref_descarte TEXT
    )
    """)

    # Tabla de Especialidades (Configuración)
    cursor.execute("DROP TABLE IF EXISTS especialidades")
    cursor.execute("""
    CREATE TABLE especialidades (
        nombre_especialidad TEXT PRIMARY KEY,
        cupos_disponibles INTEGER,
        vacantes_iniciales INTEGER
    )
    """)

    # Tabla de Resultados (Para el Reporte PDF y Tabla Principal)
    cursor.execute("DROP TABLE IF EXISTS resultados_finales")
    cursor.execute("""
    CREATE TABLE resultados_finales (
        antiguedad INTEGER,
        nombres TEXT,
        especialidad_asignada TEXT,
        motivo_asignacion TEXT
    )
    """)

    # Tabla de Auditoría (Para consulta individual)
    cursor.execute("DROP TABLE IF EXISTS auditoria_decisiones")
    cursor.execute("""
    CREATE TABLE auditoria_decisiones (
        antiguedad INTEGER,
        nombres TEXT,
        especialidad_asignada TEXT,
        opcion_1 TEXT,
        opcion_2 TEXT,
        opcion_3 TEXT,
        detalle TEXT
    )
    """)

    conn.commit()
    conn.close()