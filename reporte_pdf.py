from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
# ... otros imports ...

def generar_pdf_resultados():
    # ... inicialización de buffer y doc ...
    
    # Estilo Justificado para celdas largas
    estilo_celda = ParagraphStyle(
        "CeldaJustificada",
        parent=getSampleStyleSheet()["Normal"],
        fontSize=8,
        alignment=TA_JUSTIFY,
        leading=10
    )

    # (Lógica de obtención de datos igual que antes)

    # Creamos la tabla envolviendo el texto en Paragraph()
    tabla_data = [["Antig.", "Nombres", "Especialidad", "Motivo de Asignación"]]
    for r in datos:
        tabla_data.append([
            str(r[0]), 
            Paragraph(r[1], estilo_celda), 
            Paragraph(r[2], estilo_celda), 
            Paragraph(r[3], estilo_celda)
        ])

    # ColWidths ajustados para A4
    t = Table(tabla_data, colWidths=[40, 130, 150, 180])
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ]))
    
    # PIE DE FIRMAS (Al final del contenido)
    firmas = [
        [Paragraph("__________________________<br/>FIRMA ASPIRANTE", estilo_celda),
         Paragraph("__________________________<br/>PRESIDENTE DE JUNTA", estilo_celda)]
    ]
    t_firmas = Table(firmas, colWidths=[250, 250])
    
    contenido.append(t)
    contenido.append(Spacer(1, 50)) # Espacio antes de firmas
    contenido.append(t_firmas)

    doc.build(contenido)
    buffer.seek(0)
    return buffer
