from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import sqlite3
import io

DB = "especialidades_fae.db"

def generar_pdf_resultados():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    
    # Estilo para celdas con texto largo (Justificado)
    estilo_celda = ParagraphStyle(
        "EstiloCelda",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
        alignment=TA_JUSTIFY  # Justifica el texto dentro de la celda
    )

    estilo_titulo = ParagraphStyle("Titulo", parent=styles["Normal"], alignment=TA_CENTER, fontSize=12, fontName="Helvetica-Bold")

    contenido = []
    contenido.append(Paragraph("FUERZA AÉREA ECUATORIANA", estilo_titulo))
    contenido.append(Paragraph("REPORTE OFICIAL DE ASIGNACIÓN DE ESPECIALIDADES", estilo_titulo))
    contenido.append(Spacer(1, 20))

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT antiguedad, nombres, especialidad_asignada, motivo_asignacion FROM resultados_finales ORDER BY antiguedad ASC")
    datos = cursor.fetchall()
    conn.close()

    # Encabezados con Paragraph para que respeten el estilo
    tabla_data = [[
        Paragraph("<b>Antig.</b>", estilo_celda),
        Paragraph("<b>Nombres</b>", estilo_celda),
        Paragraph("<b>Especialidad</b>", estilo_celda),
        Paragraph("<b>Motivo de Asignación</b>", estilo_celda)
    ]]
    
    for r in datos:
        tabla_data.append([
            Paragraph(str(r[0]), estilo_celda),
            Paragraph(r[1], estilo_celda),
            Paragraph(r[2], estilo_celda),
            Paragraph(r[3], estilo_celda)
        ])

    # Ajuste de anchos para evitar desbordamiento
    t = Table(tabla_data, colWidths=[40, 130, 160, 160])
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'), # Alineación superior para textos largos
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ]))
    contenido.append(t)
    
    # SECCIÓN DE FIRMAS
    contenido.append(Spacer(1, 50))
    firma_data = [[
        Paragraph("__________________________<br/>FIRMA DEL ASPIRANTE", estilo_titulo),
        Paragraph("__________________________<br/>PRESIDENTE DE JUNTA", estilo_titulo)
    ]]
    t_firma = Table(firma_data, colWidths=[245, 245])
    contenido.append(t_firma)

    doc.build(contenido)
    buffer.seek(0)
    return buffer