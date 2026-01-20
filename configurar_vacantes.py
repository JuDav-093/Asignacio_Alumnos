import sqlite3

def establecer_cupos():
    conn = sqlite3.connect('especialidades_fae.db')
    cursor = conn.cursor()

    # Definición extendida de vacantes según tus archivos Excel
    # El total debe sumar 68 alumnos
    vacantes = [
        ('DEFENSA AEREA', 5, 5),
        ('METEOROLOGIA', 3, 3),
        ('COMUNICACIONES', 4, 4),
        ('MECANICA', 20, 20),
        ('ARMAMENTO', 3, 3),
        ('PERSONAL', 4, 4),
        ('ELECTRONICA', 6, 6),
        ('ABASTECIMIENTOS', 4, 4),
        ('OPERACIONES DE INTELIGENCIA Y CONTRAINTELIGENCIA', 4, 4),
        ('MANTENIMIENTO RADAR', 3, 3), 
        ('DESPACHADOR DE AERONAVES', 4, 4), 
        ('TRANSITO AEREO', 3, 3),
        ('ESTRUCTURAS', 3, 3),
        ('DESARROLLO Y SOSTENIMIENTO ESPACIAL', 2, 2)
    ]

    cursor.execute("DELETE FROM cupos")
    cursor.executemany("INSERT INTO cupos VALUES (?, ?, ?)", vacantes)
    conn.commit()
    cursor.execute("SELECT SUM(vacantes_iniciales) FROM cupos")
    total = cursor.fetchone()[0]
    print(f"Total de cupos configurados: {total}")
    conn.close()

if __name__ == "__main__":
    establecer_cupos()