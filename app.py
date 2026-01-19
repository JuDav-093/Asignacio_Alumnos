import streamlit as st
import pandas as pd
import sqlite3
import os
from reporte_pdf import generar_pdf_resultados
# Importa tus funciones de los otros archivos
from algoritmo_asignacion import ejecutar_asignacion 

st.set_page_config(page_title="Asignación FAE", page_icon="✈️")

# --- BARRA LATERAL ---
st.sidebar.title("Navegación")
paso = st.sidebar.radio("Ir a:", ["Panel de Control", "Resultados y Reportes"])

if paso == "Panel de Control":
    st.title("🕹️ Panel de Control de Asignación")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Preparación")
        if st.button("Configurar Base de Datos y Vacantes"):
            # Aquí llamas a crear_db e inicializar cupos
            st.success("Sistema listo para recibir datos.")

    with col2:
        st.subheader("2. Carga de Archivos")
        if st.button("Procesar Excels Locales"):
            # Aquí llamas a tu script cargar_todo() modificado
            st.success("Datos cargados correctamente.")

    st.divider()
    st.subheader("3. Ejecución")
    if st.button("⚡ EJECUTAR ASIGNACIÓN AUTOMÁTICA"):
        ejecutar_asignacion()
        st.balloons()
        st.success("Proceso terminado. Diríjase a 'Resultados' para descargar el informe.")

elif paso == "Resultados y Reportes":
    st.title("📄 Resultados Finales")
    
    if os.path.exists('especialidades_fae.db'):
        conn = sqlite3.connect('especialidades_fae.db')
        df = pd.read_sql_query("SELECT * FROM resultados_finales", conn)
        st.dataframe(df, use_container_width=True)
        
        # BOTÓN PARA PDF
        pdf_data = generar_pdf_resultados()
        st.download_button(
            label="📥 Descargar Reporte PDF Oficial",
            data=pdf_data,
            file_name="Reporte_Asignacion_FAE.pdf",
            mime="application/pdf"
        )
        conn.close()
    else:
        st.error("Aún no hay resultados. Ejecute la asignación primero.")