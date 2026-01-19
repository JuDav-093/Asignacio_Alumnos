from fpdf import FPDF
import sqlite3
import pandas as pd
from datetime import datetime

class ReporteFAE(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'FUERZA AÉREA ECUATORIANA', 0, 1, 'C')
        self.cell(0, 10, 'JUNTA ACADÉMICA - ASIGNACIÓN DE ESPECIALIDADES', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def generar_pdf_resultados():
    conn = sqlite3.connect('especialidades_fae.db')
    df = pd.read_sql_query("SELECT * FROM resultados_finales", conn)
    conn.close()

    pdf = ReporteFAE()
    pdf.add_page()
    pdf.set_font('Arial', '', 10)

    # Encabezados de tabla
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(30, 10, 'Antigüedad', 1, 0, 'C', True)
    pdf.cell(80, 10, 'Nombres y Apellidos', 1, 0, 'C', True)
    pdf.cell(80, 10, 'Especialidad Asignada', 1, 1, 'C', True)

    # Datos
    for _, row in df.iterrows():
        pdf.cell(30, 10, str(row['antiguedad']), 1, 0, 'C')
        pdf.cell(80, 10, str(row['nombres']), 1, 0, 'L')
        pdf.cell(80, 10, str(row['especialidad_asignada']), 1, 1, 'L')

    pdf.ln(20)
    pdf.cell(0, 10, '__________________________', 0, 1, 'C')
    pdf.cell(0, 10, 'Firma de la Junta Académica', 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1')