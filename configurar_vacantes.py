import sqlite3

DB = "especialidades_fae.db"

def establecer_cupos():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM especialidades")

    especialidades = [
        ('TRANSITO AEREO', 3), ('METEOROLOGIA', 3), ('DEFENSA AEREA', 5),
        ('MECANICA', 20), ('ELECTRONICA', 6), ('MANTENIMIENTO RADAR', 3),
        ('ARMAMENTO', 3), ('DESARROLLO Y SOSTENIMIENTO ESPACIAL', 2),
        ('ESTRUCTURAS', 3), ('DESPACHADOR DE AERONAVES', 4),
        ('COMUNICACIONES', 4), ('ABASTECIMIENTOS', 4), ('PERSONAL', 4),
        ('OPERACIONES DE INTELIGENCIA Y CONTRAINTELIGENCIA', 4)
    ]

    for nombre, cupo in especialidades:
        cursor.execute("INSERT INTO especialidades VALUES (?, ?, ?)", (nombre, cupo, cupo))

    conn.commit()
    conn.close()