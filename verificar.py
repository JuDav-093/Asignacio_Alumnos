import sqlite3

def consultar_alumnos():
    conn = sqlite3.connect('especialidades_fae.db')
    cursor = conn.cursor()
    
    # Consulta simple para ver los primeros 5 alumnos cargados
    cursor.execute("SELECT * FROM preferencias LIMIT 5")
    rows = cursor.fetchall()
    
    for row in rows:
        print(f"Antigüedad: {row[0]} | Opción 1: {row[1]} | Opción 2: {row[2]}")
        
    conn.close()

if __name__ == "__main__":
    consultar_alumnos()