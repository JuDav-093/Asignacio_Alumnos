import os
import sqlite3
import pandas as pd
# Importamos las funciones de tus otros archivos
from crear_db import inicializar_db
from configurar_vacantes import establecer_cupos
from cargar_datos import cargar_todo
from algoritmo_asignacion import ejecutar_asignacion

def menu_principal():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==================================================")
        print("   SISTEMA DE ASIGNACIÓN DE ESPECIALIDADES - FAE  ")
        print("==================================================")
        print("1. Inicializar Base de Datos (Borra datos previos)")
        print("2. Configurar Vacantes Institucionales (68 cupos)")
        print("3. Cargar Datos (Antigüedades, BAT-7, Afinidad)")
        print("4. EJECUTAR ALGORITMO DE ASIGNACIÓN")
        print("5. Exportar Resultados a Excel")
        print("6. Salir")
        print("==================================================")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            confirmar = input("¿Está seguro? Esto borrará todo (s/n): ")
            if confirmar.lower() == 's':
                if os.path.exists('especialidades_fae.db'):
                    os.remove('especialidades_fae.db')
                inicializar_db()
                input("\nPresione Enter para continuar...")
        
        elif opcion == "2":
            establecer_cupos()
            input("\nPresione Enter para continuar...")
            
        elif opcion == "3":
            cargar_todo()
            input("\nPresione Enter para continuar...")
            
        elif opcion == "4":
            ejecutar_asignacion()
            input("\nPresione Enter para continuar...")
            
        elif opcion == "5":
            exportar_a_excel()
            input("\nPresione Enter para continuar...")
            
        elif opcion == "6":
            print("Saliendo del sistema...")
            break

def exportar_a_excel():
    try:
        conn = sqlite3.connect('especialidades_fae.db')
        # Consulta que une los resultados con los nombres originales
        query = "SELECT * FROM resultados_finales ORDER BY antiguedad ASC"
        df = pd.read_sql_query(query, conn)
        
        nombre_archivo = 'MATRIZ_ASIGNACION_FINAL.xlsx'
        df.to_excel(nombre_archivo, index=False)
        
        print(f"✔ Éxito: Se ha generado el archivo '{nombre_archivo}'")
        conn.close()
    except Exception as e:
        print(f"❌ Error al exportar: {e}")

if __name__ == "__main__":
    menu_principal()