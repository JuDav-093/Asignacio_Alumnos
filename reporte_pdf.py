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

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "Titulo",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=12,
        leading=14,
        fontName="Helvetica-Bold"
    )

    estilo_tabla = ParagraphStyle(
        "Tabla",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
        alignment=TA_JUSTIFY
    )

    contenido = []

    # ===== ENCABEZADO =====
    contenido.append(Paragraph(
        "FUERZA AÉREA ECUATORIANA<br/>"
        "JUNTA ACADÉMICA<br/><br/>"
        "REPORTE OFICIAL DE ASIGNACIÓN DE ESPECIALIDADES",
        estilo_titulo
    ))

    fecha = datetime.now().strftime("%d/%m/%Y")
    contenido.append(Paragraph(f"Fecha de emisión: {fecha}<br/><br/>", styles["Normal"]))

    # ===== DATOS =====
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            antiguedad,
            nombres,
            especialidad_asignada,
            motivo_asignacion
        FROM resultados_finales
        ORDER BY antiguedad
    """)

    datos = cursor.fetchall()
    conn.close()

    tabla_data = [[
        Paragraph("<b>Antig.</b>", estilo_tabla),
        Paragraph("<b>Nombres</b>", estilo_tabla),
        Paragraph("<b>Especialidad</b>", estilo_tabla),
        Paragraph("<b>Motivo de Asignación</b>", estilo_tabla)
    ]]

    for a, n, e, m in datos:
        tabla_data.append([
            Paragraph(str(a), estilo_tabla),
            Paragraph(n, estilo_tabla),
            Paragraph(e, estilo_tabla),
            Paragraph(m, estilo_tabla)
        ])

    tabla = Table(
        tabla_data,
        colWidths=[40, 140, 160, 160]
    )

    tabla.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("ALIGN", (0,0), (0,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))

    contenido.append(tabla)

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
