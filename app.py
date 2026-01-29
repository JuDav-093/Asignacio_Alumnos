import streamlit as st
import pandas as pd
import sqlite3
import os

# ===== IMPORTACIÓN DE TUS MÓDULOS =====
from crear_db import inicializar_db
from configurar_vacantes import establecer_cupos
from cargar_datos import cargar_desde_excel
from algoritmo_asignacion import ejecutar_asignacion
from reporte_pdf import generar_pdf_resultados
from estadisticas import obtener_estadisticas
from auditoria import obtener_auditoria

DB = "especialidades_fae.db"

# ===== CONFIGURACIÓN DE PÁGINA =====
st.set_page_config(
    page_title="Sistema de Asignación FAE",
    page_icon="✈️",
    layout="wide"
)

# ===== ESTILO INSTITUCIONAL FAE (CSS) =====
st.markdown("""
<style>
    .stApp { background-color: #ECEFF1; }
    
    /* SideBar */
    [data-testid="stSidebar"] {
        background-color: #002B5B;
        min-width: 300px;
    }
    [data-testid="stSidebar"] * { color: white; }

    /* Contenedores de secciones */
    .block-container { padding: 2rem 3rem; }
    
    section[data-testid="stVerticalBlock"] > div {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Títulos */
    h1 { color: #002B5B; border-bottom: 3px solid #002B5B; }
    
    /* El recuadro azul de Auditoría (st.info) */
    .stAlert {
        background-color: #E3F2FD !important;
        color: #0D47A1 !important;
        border-left: 5px solid #1976D2 !important;
    }
</style>
""", unsafe_allow_html=True)

# ===== BARRA LATERAL (SIDEBAR) =====
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Logo_de_la_Fuerza_A%C3%A9rea_Ecuatoriana.svg/1200px-Logo_de_la_Fuerza_A%C3%A9rea_Ecuatoriana.svg.png", width=100)
    st.title("Sistema FAE")
    paso = st.radio(
        "Seleccione una etapa:",
        [
            "1️⃣ Carga de Datos",
            "2️⃣ Ejecutar Asignación",
            "3️⃣ Resultados y Reportes",
            "4️⃣ Auditoría y Estadísticas"
        ]
    )
    st.divider()
    st.markdown("### Sistema de Apoyo a la Junta Académica")
    st.caption("Criterios Aplicados:")
    st.markdown("* Antigüedad\n* Preferencia del Alumno\n* BAT-7\n* Disponibilidad de Cupos")

# =========================================================
# 1️⃣ ETAPA: CARGA DE DATOS
# =========================================================
if paso == "1️⃣ Carga de Datos":
    st.title("📥 Carga de Información")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("📘 Antigüedades")
        file_ant = st.file_uploader("Excel Antigüedades", type="xlsx", key="ant")
    with col2:
        st.subheader("📗 Perfil BAT-7")
        file_bat = st.file_uploader("Excel BAT-7", type="xlsx", key="bat")
    with col3:
        st.subheader("📕 Afinidad")
        file_afin = st.file_uploader("Excel Afinidad", type="xlsx", key="afin")

    if st.button("📥 Procesar y Guardar", type="primary"):
        if file_ant and file_bat and file_afin:
            with st.spinner("Inicializando base de datos..."):
                inicializar_db()
                establecer_cupos()
                ok = cargar_desde_excel(file_ant, file_bat, file_afin)
                if ok:
                    st.success("✈️ Información cargada correctamente.")
                    st.balloons()
                else:
                    st.error("Error al procesar archivos. Verifique el formato.")
        else:
            st.warning("Cargue los tres archivos obligatorios.")

# =========================================================
# 2️⃣ ETAPA: EJECUCIÓN
# =========================================================
elif paso == "2️⃣ Ejecutar Asignación":
    st.title("⚙️ Motor de Asignación")
    st.info("El algoritmo procesará a los alumnos en orden de antigüedad (ASC) y asignará la mejor especialidad según puntaje ponderado.")
    
    if st.button("⚡ INICIAR PROCESO", type="primary", use_container_width=True):
        if ejecutar_asignacion():
            st.success("Asignación completada con éxito.")
            st.toast("Proceso Finalizado", icon="✈️")
        else:
            st.error("Error en la ejecución.")

# =========================================================
# 3️⃣ ETAPA: RESULTADOS
# =========================================================
elif paso == "3️⃣ Resultados y Reportes":
    st.title("📋 Resultados Finales")
    if not os.path.exists(DB):
        st.warning("Base de datos no encontrada.")
    else:
        conn = sqlite3.connect(DB)
        df = pd.read_sql("SELECT * FROM resultados_finales ORDER BY antiguedad", conn)
        conn.close()

        if df.empty:
            st.info("No hay resultados generados aún.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.subheader("📥 Descargas")
            c1, c2 = st.columns(2)
            with c1:
                pdf_buf = generar_pdf_resultados()
                st.download_button("📄 Descargar PDF Oficial", pdf_buf, "Reporte_FAE.pdf", "application/pdf")
            with c2:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📊 Descargar CSV", csv, "Resultados.csv", "text/csv")

# =========================================================
# 4️⃣ ETAPA: AUDITORÍA Y ESTADÍSTICAS
# =========================================================
elif paso == "4️⃣ Auditoría y Estadísticas":
    st.title("📊 Auditoría por Estudiante")
    
    # --- Parte 1: Auditoría Detallada ---
    antig = st.number_input("Ingrese Antigüedad del Alumno a consultar", min_value=1, step=1)
    
    if st.button("🔍 Consultar Motivo"):
        asp, res, det = obtener_auditoria(antig)
        
        if asp.empty:
            st.error("Alumno no encontrado en los registros.")
        else:
            # Layout similar a tu imagen de referencia
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Datos y Preferencias:**")
                st.table(asp)
            with c2:
                st.markdown("**Resultado de Asignación:**")
                st.table(res)
            
            # EL RECUADRO AZUL (Detalle del Cálculo)
            if not det.empty:
                st.markdown("### Detalle del Cálculo:")
                st.info(det.iloc[0]['detalle'])

    st.divider()
    st.subheader("📈 Resumen de Vacantes")

    # Llamada directa a las estadísticas
    df_stats = obtener_estadisticas()

    if df_stats["Alumnos Asignados"].sum() == 0:
        st.info("Ejecute la asignación en la Etapa 2 para ver el resumen de vacantes.")
    else:
        st.dataframe(
            df_stats, 
            use_container_width=True, 
            hide_index=True
        )