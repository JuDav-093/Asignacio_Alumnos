from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import sqlite3
import io
from datetime import datetime

DB = "especialidades_fae.db"

def generar_pdf_resultados():
    buffer = io.BytesIO()

    # Configuración del documento con márgenes adecuados
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Estilos personalizados
    estilo_titulo = ParagraphStyle(
        "Titulo",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=12,
        leading=14,
        fontName="Helvetica-Bold"
    )

    # Estilo clave para que el texto NO se salga de la celda (Justificado)
    estilo_celda = ParagraphStyle(
        "EstiloCelda",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
        alignment=TA_LEFT # O TA_JUSTIFY si prefieres bloques cuadrados
    )

    contenido = []

    # ===== ENCABEZADO INSTITUCIONAL =====
    contenido.append(Paragraph("FUERZA AÉREA ECUATORIANA", estilo_titulo))
    contenido.append(Paragraph("JUNTA ACADÉMICA", estilo_titulo))
    contenido.append(Spacer(1, 12))
    contenido.append(Paragraph("REPORTE OFICIAL DE ASIGNACIÓN DE ESPECIALIDADES", estilo_titulo))
    contenido.append(Spacer(1, 12))

    fecha = datetime.now().strftime("%d/%m/%Y")
    contenido.append(Paragraph(f"Fecha de emisión: {fecha}", styles["Normal"]))
    contenido.append(Spacer(1, 15))

    # ===== OBTENCIÓN DE DATOS =====
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Usamos los nombres exactos de columnas definidos en crear_db.py
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

    # Definición de la tabla (Encabezados)
    # Envolvemos los encabezados en Paragraph para mantener el estilo
    tabla_data = [[
        Paragraph("<b>Antig.</b>", estilo_celda),
        Paragraph("<b>Nombres</b>", estilo_celda),
        Paragraph("<b>Especialidad</b>", estilo_celda),
        Paragraph("<b>Motivo de Asignación</b>", estilo_celda)
    ]]

    # Llenado de filas: Cada celda de texto se envuelve en un Paragraph para que haga wrap
    for a, n, e, m in datos:
        tabla_data.append([
            Paragraph(str(a), estilo_celda),
            Paragraph(n, estilo_celda),
            Paragraph(e, estilo_celda),
            Paragraph(m, estilo_celda)
        ])

    # Configuración de anchos de columna (Suma total aproximada de 530 puntos para A4)
    tabla = Table(
        tabla_data, 
        colWidths=[40, 140, 160, 160],
        repeatRows=1 # Repite el encabezado si hay más de una página
    )

    tabla.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "TOP"), # Alineación al tope para textos largos
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))

    contenido.append(tabla)

    # ===== SECCIÓN DE FIRMAS (Pie de página) =====
    contenido.append(Spacer(1, 60)) # Espacio amplio para las firmas

    # Tabla invisible para organizar las firmas
    estilo_firma = ParagraphStyle("Firma", parent=styles["Normal"], alignment=TA_CENTER, fontSize=10)
    
    data_firmas = [[
        Paragraph("______________________________<br/>FIRMA DEL ASPIRANTE", estilo_firma),
        Paragraph("______________________________<br/>PRESIDENTE JUNTA ACADÉMICA", estilo_firma)
    ]]

    tabla_firmas = Table(data_firmas, colWidths=[250, 250])
    contenido.append(tabla_firmas)

    # Construcción final del PDF
    doc.build(contenido)
    buffer.seek(0)
    return buffer
