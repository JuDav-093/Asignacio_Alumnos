from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import sqlite3
import io
from datetime import datetime

DB = "especialidades_fae.db"

def generar_pdf_resultados():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Estilos de texto
    estilo_titulo = ParagraphStyle("Titulo", parent=styles["Normal"], alignment=TA_CENTER, fontSize=14, fontName="Helvetica-Bold")
    estilo_tabla = ParagraphStyle("Tabla", parent=styles["Normal"], fontSize=9)

    contenido = []
    contenido.append(Paragraph("FUERZA AÉREA ECUATORIANA", estilo_titulo))
    contenido.append(Paragraph("REPORTE OFICIAL DE ASIGNACIÓN<br/><br/>", estilo_titulo))

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    # CONSULTA CORREGIDA: coincide con crear_db.py
    cursor.execute("""
        SELECT antiguedad, nombres, especialidad_asignada, motivo_asignacion 
        FROM resultados_finales 
        ORDER BY antiguedad ASC
    """)
    datos = cursor.fetchall()
    conn.close()

    # Encabezados de tabla
    tabla_data = [["Antig.", "Nombres", "Especialidad", "Motivo"]]
    
    for fila in datos:
        tabla_data.append([str(fila[0]), fila[1], fila[2], fila[3]])

    t = Table(tabla_data, colWidths=[50, 150, 150, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    contenido.append(t)


    # ===== FIRMAS =====

    contenido.append(Paragraph("<br/><br/>", styles["Normal"]))

    contenido.append(Paragraph(

        "______________________________<br/>"

        "PRESIDENTE JUNTA ACADÉMICA",

        styles["Normal"]

    ))



    doc.build(contenido)

    buffer.seek(0)

    return buffer

