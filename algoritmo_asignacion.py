import sqlite3

DB = "especialidades_fae.db"

PESOS = {"antiguedad": 0.30, "bat": 0.20, "afinidad": 0.15, "necesidad": 0.35}

PRIORIDAD_INST = [
    'TRANSITO AEREO', 'METEOROLOGIA', 'DEFENSA AEREA', 'MECANICA', 'ELECTRONICA',
    'MANTENIMIENTO RADAR', 'ARMAMENTO', 'DESARROLLO Y SOSTENIMIENTO ESPACIAL',
    'ESTRUCTURAS', 'DESPACHADOR DE AERONAVES', 'COMUNICACIONES', 'ABASTECIMIENTOS',
    'PERSONAL', 'OPERACIONES DE INTELIGENCIA Y CONTRAINTELIGENCIA'
]

def ejecutar_asignacion():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM resultados_finales")
    cursor.execute("DELETE FROM auditoria_decisiones")

    cursor.execute("SELECT nombre_especialidad, cupos_disponibles FROM especialidades")
    cupos = dict(cursor.fetchall())

    cursor.execute("SELECT * FROM aspirantes ORDER BY antiguedad ASC")
    aspirantes = cursor.fetchall()

    for asp in aspirantes:
        ant, nombre, b_p, b_o, b_s, p_p, p_o, p_d = asp
        mejor_puntaje = -1
        asignada = None
        info_calculo = ""

        for esp in PRIORIDAD_INST:
            if cupos.get(esp, 0) <= 0: continue

            v_ant = (1 / ant) * PESOS["antiguedad"]
            v_bat = PESOS["bat"] if esp in [b_p, b_o, b_s] else 0
            v_afin = PESOS["afinidad"] if esp in [p_p, p_o] else 0
            v_nec = ((len(PRIORIDAD_INST) - PRIORIDAD_INST.index(esp)) / len(PRIORIDAD_INST)) * PESOS["necesidad"]
            
            total = v_ant + v_bat + v_afin + v_nec

            if total > mejor_puntaje:
                mejor_puntaje = total
                asignada = esp
                info_calculo = (
                    f"**Especialidad asignada: {esp}**\n\n"
                    f"Especialidad 2DA OPCIÓN: {p_o} | Especialidad 3RA OPCIÓN: {p_d}\n\n"
                    f"Antigüedad: {round(v_ant,3)} (30%) | BAT-7: {round(v_bat,3)} (20%) | "
                    f"Afinidad: {round(v_afin,3)} (15%) | Necesidad: {round(v_nec,3)} (35%) |\n\n"
                    f"Prioridad Especialidad: {PRIORIDAD_INST.index(esp)+1} | Cupos restantes luego: {cupos[esp]-1}"
                )

        if asignada:
            cupos[asignada] -= 1
            # Inserción con nombres corregidos
            cursor.execute("""
                INSERT INTO resultados_finales VALUES (?, ?, ?, ?)
            """, (ant, nombre, asignada, "Ponderación Académica"))
            
            cursor.execute("""
                INSERT INTO auditoria_decisiones VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (ant, nombre, asignada, p_p, p_o, p_d, info_calculo))

    conn.commit()
    conn.close()
    return True