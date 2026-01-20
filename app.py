import streamlit as st
import pandas as pd
import sqlite3
import os

# ===== MÓDULOS DEL SISTEMA =====
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

# ===== ESTILO INSTITUCIONAL FAE =====
st.markdown("""
<style>
    body {
        background-color: #ECEFF1;
    }

    .stApp {
        background-color: #ECEFF1;
    }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background-color: #002B5B;
        min-width: 300px;
        max-width: 300px;
    }

    [data-testid="stSidebar"] * {
        color: white;
        font-size: 16px;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-size: 20px;
        font-weight: bold;
        color: #E3F2FD;
    }

    /* ===== TITULOS PRINCIPALES ===== */
    h1 {
        color: #002B5B;
        font-size: 32px;
        font-weight: bold;
        border-bottom: 3px solid #002B5B;
        padding-bottom: 6px;
    }

    h2 {
        color: #003366;
        font-size: 26px;
        font-weight: bold;
    }

    h3 {
        color: #003366;
        font-size: 22px;
        font-weight: bold;
    }

    /* ===== CONTENEDORES ===== */
    .block-container {
        padding: 2.5rem 3rem;
    }

    section[data-testid="stVerticalBlock"] > div {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 6px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    /* ===== BOTONES ===== */
    .stButton>button {
        background-color: #002B5B;
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px 18px;
        border: none;
    }

    .stButton>button:hover {
        background-color: #001B3A;
        color: white;
    }

    /* ===== INFO / WARNING ===== */
    .stAlert {
        font-size: 15px;
    }

</style>
""", unsafe_allow_html=True)


# ===== BARRA LATERAL =====
with st.sidebar:
    st.title("✈️ Sistema FAE")
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
    st.info(
        "Sistema de apoyo a la Junta Académica\n\n"
        "Criterios aplicados:\n"
        "• Antigüedad\n"
        "• Preferencias del alumno\n"
        "• Perfil BAT-7\n"
        "• Disponibilidad de cupos"
    )

# =========================================================
# 1️⃣ CARGA DE DATOS
# =========================================================
if paso == "1️⃣ Carga de Datos":
    st.title("📥 Carga de Información Académica")

    st.subheader("📘 Antigüedades")
    st.info(
        "Archivo Excel (.xlsx)\n"
        "Columnas obligatorias:\n"
        "• antiguedad (entero)\n"
        "• nombres (texto)\n"
        "Una fila por alumno."
    )
    file_ant = st.file_uploader("Cargar archivo de Antigüedades", type="xlsx")

    st.subheader("📗 BAT-7 (Aptitudes)")
    st.info(
        "Archivo Excel (.xlsx)\n"
        "Fila 1: encabezado institucional\n"
        "Fila 2:\n"
        "antiguedad | PRINCIPAL | OPTATIVA 1 | SUGERENCIA"
    )
    file_bat = st.file_uploader("Cargar archivo BAT-7", type="xlsx")

    st.subheader("📕 Afinidad del Alumno")
    st.info(
        "Archivo Excel (.xlsx)\n"
        "Fila 1: encabezado institucional\n"
        "Fila 2:\n"
        "antiguedad | PRINCIPAL | OPTATIVA 1 | DESCARTE"
    )
    file_afin = st.file_uploader("Cargar archivo de Afinidad", type="xlsx")

    if st.button("📥 Procesar y Guardar Información", type="primary"):
        if not (file_ant and file_bat and file_afin):
            st.warning("⚠️ Debe cargar los TRES archivos Excel.")
        else:
            try:
                inicializar_db()
                establecer_cupos()
                ok = cargar_desde_excel(file_ant, file_bat, file_afin)

                if ok:
                    st.success("✈️ Información cargada correctamente en el sistema.")
                else:
                    st.error("❌ Error al procesar los archivos.")
            except Exception as e:
                st.error(f"Error crítico: {e}")

# =========================================================
# 2️⃣ EJECUTAR ASIGNACIÓN
# =========================================================
elif paso == "2️⃣ Ejecutar Asignación":
    st.title("⚙️ Ejecución del Motor de Asignación")

    st.info(
        "El sistema asignará especialidades considerando:\n"
        "• Orden de antigüedad\n"
        "• Preferencias del alumno\n"
        "• Perfil BAT-7\n"
        "• Cupos disponibles\n\n"
        "✔ Ningún alumno quedará sin especialidad."
    )

    if st.button("⚡ EJECUTAR ASIGNACIÓN", type="primary"):
        with st.spinner("Procesando asignaciones..."):
            try:
                exito = ejecutar_asignacion()
                if exito:
                    st.success("✈️ Asignación completada conforme a normativa institucional.")
                    st.toast("Proceso aprobado por el sistema", icon="✈️")
                else:
                    st.error("❌ No se pudo completar la asignación.")
            except Exception as e:
                st.error(f"Error durante la asignación: {e}")

# =========================================================
# 3️⃣ RESULTADOS Y REPORTES
# =========================================================
elif paso == "3️⃣ Resultados y Reportes":
    st.title("📄 Resultados Finales")

    if not os.path.exists(DB):
        st.warning("⚠️ No existe base de datos. Ejecute las etapas previas.")
    else:
        conn = sqlite3.connect(DB)
        try:
            df = pd.read_sql(
                "SELECT * FROM resultados_finales ORDER BY antiguedad",
                conn
            )
            conn.close()

            if df.empty:
                st.warning("No existen resultados disponibles.")
            else:
                st.subheader("📋 Asignación de Especialidades")
                st.dataframe(df, use_container_width=True)

                st.divider()
                st.subheader("📥 Descargas Oficiales")

                col1, col2 = st.columns(2)

                with col1:
                    pdf = generar_pdf_resultados()
                    st.download_button(
                        "📄 Descargar Reporte PDF Oficial",
                        pdf,
                        file_name="Reporte_Asignacion_FAE.pdf",
                        mime="application/pdf"
                    )

                with col2:
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "📊 Descargar Resultados en CSV",
                        csv,
                        file_name="Resultados_Asignacion_FAE.csv",
                        mime="text/csv"
                    )

        except Exception as e:
            st.error(f"Error al cargar resultados: {e}")

# =========================================================
# 4️⃣ AUDITORÍA Y ESTADÍSTICAS
# =========================================================
elif paso == "4️⃣ Auditoría y Estadísticas":
    st.title("🧠 Auditoría y 📊 Estadísticas")

    st.subheader("📊 Estadísticas por Especialidad")
    try:
        df_stats = obtener_estadisticas()
        st.dataframe(df_stats, use_container_width=True)
    except Exception as e:
        st.warning(f"No se pudieron cargar estadísticas: {e}")

    st.divider()

    st.subheader("🧠 Auditoría de Decisiones por Alumno")
    antig = st.number_input(
        "Ingrese la antigüedad del alumno",
        min_value=1,
        step=1
    )

    if st.button("🔍 Consultar Auditoría"):
        alumno, bat, pref, res = obtener_auditoria(antig)

        if alumno.empty:
            st.warning("Alumno no encontrado.")
        else:
            st.markdown("### 👤 Alumno")
            st.table(alumno)

            st.markdown("### 🎯 Preferencias")
            st.table(pref)

            st.markdown("### 🧠 Perfil BAT-7")
            st.table(bat)

            st.markdown("### ✅ Resultado Final")
            st.table(res)
