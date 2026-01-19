import sqlite3

def establecer_cupos():
    conn = sqlite3.connect('especialidades_fae.db')
    cursor = conn.cursor()

    # Repartición de 68 cupos según necesidad institucional
    vacantes = [
        ('DEFENSA AEREA', 10, 10),
        ('COMUNICACIONES', 8, 8),
        ('MECANICA DE AVIACION', 15, 15),
        ('ARMAMENTO AEREO', 5, 5),
        ('PERSONAL', 5, 5),
        ('INFANTERIA AEREA', 10, 10),
        ('ELECTRONICA', 5, 5),
        ('ABASTECIMIENTOS', 4, 4),
        ('INFORMATICA', 3, 3),
        ('INTELIGENCIA', 3, 3)
    ]

    cursor.execute("DELETE FROM cupos")
    cursor.executemany("INSERT INTO cupos VALUES (?, ?, ?)", vacantes)
    conn.commit()
    
    # Verificación
    cursor.execute("SELECT SUM(vacantes_iniciales) FROM cupos")
    total = cursor.fetchone()[0]
    print(f"Total de cupos configurados: {total} (Debe ser 68)")
    
    conn.close()

if __name__ == "__main__":
    establecer_cupos()