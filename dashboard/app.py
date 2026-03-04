import os
import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# CONFIGURACIÓN DE PÁGINA
# ==============================
st.set_page_config(page_title="Sistema Inteligente Logístico", layout="wide")

st.title("🚛 Sistema Inteligente de Control Operativo Logístico")
st.markdown("### Panel Ejecutivo de Operaciones")

# ==============================
# CARGAR DATOS
# ==============================

@st.cache_data
def cargar_datos():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(BASE_DIR, "data", "raw", "operaciones_logisticas.xlsx")
    df = pd.read_excel(ruta)
    return df

df = cargar_datos()





# ==============================
# KPIs PRINCIPALES
# ==============================
total_operaciones = len(df)
total_ingreso = df["Ingreso"].sum()
total_utilidad = df["Utilidad"].sum()
porcentaje_sla = (df["Cumple_SLA"].value_counts(normalize=True).get("Sí", 0)) * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Operaciones", f"{total_operaciones:,}")
col2.metric("Ingreso Total", f"S/ {total_ingreso:,.0f}")
col3.metric("Utilidad Total", f"S/ {total_utilidad:,.0f}")
col4.metric("% Cumplimiento SLA", f"{porcentaje_sla:.2f}%")

# =====================================
# INDICADOR GENERAL DEL NEGOCIO
# =====================================

margen = (total_utilidad / total_ingreso) * 100 if total_ingreso != 0 else 0

st.subheader("📌 Estado General del Negocio")

if margen > 25:
    st.success(f"🟢 Negocio Saludable | Margen: {margen:.2f}%")
elif margen > 10:
    st.warning(f"🟡 Margen Moderado | Margen: {margen:.2f}%")
else:
    st.error(f"🔴 Margen Crítico | Margen: {margen:.2f}%")

st.divider()

# ==============================
# ALERTAS INTELIGENTES
# ==============================
if porcentaje_sla < 85:
    st.error(f"⚠️ ALERTA: Cumplimiento SLA bajo ({porcentaje_sla:.2f}%)")
else:
    st.success(f"✅ Cumplimiento SLA saludable ({porcentaje_sla:.2f}%)")

st.divider()

# ==============================
# FILTROS LATERALES
# ==============================
st.sidebar.header("Filtros")

ruta = st.sidebar.multiselect("Ruta", df["Ruta"].unique())
conductor = st.sidebar.multiselect("Conductor", df["Conductor"].unique())
estado = st.sidebar.multiselect("Estado", df["Estado"].unique())

df_filtrado = df.copy()

if ruta:
    df_filtrado = df_filtrado[df_filtrado["Ruta"].isin(ruta)]

if conductor:
    df_filtrado = df_filtrado[df_filtrado["Conductor"].isin(conductor)]

if estado:
    df_filtrado = df_filtrado[df_filtrado["Estado"].isin(estado)]




# ==============================
# GRÁFICOS PRINCIPALES
# ==============================
colA, colB = st.columns(2)

with colA:
    fig_rutas = px.bar(
        df_filtrado.groupby("Ruta")["Utilidad"].sum().reset_index(),
        x="Ruta",
        y="Utilidad",
        title="Utilidad por Ruta",
        text_auto=True
    )
    st.plotly_chart(fig_rutas, use_container_width=True)

with colB:
    fig_estado = px.pie(
        df_filtrado,
        names="Estado",
        title="Distribución de Entregas"
    )
    st.plotly_chart(fig_estado, use_container_width=True)

st.divider()

# ==============================
# TENDENCIA MENSUAL DE INGRESOS
# ==============================
df_filtrado["Mes"] = df_filtrado["Fecha_Entrega"].dt.month
tendencia = df_filtrado.groupby("Mes")["Ingreso"].sum().reset_index()

fig_tendencia = px.line(
    tendencia,
    x="Mes",
    y="Ingreso",
    title="📈 Tendencia Mensual de Ingresos",
    markers=True
)
st.plotly_chart(fig_tendencia, use_container_width=True)

st.divider()

# ==============================
# RANKING DE CONDUCTORES
# ==============================
st.subheader("🏆 Ranking de Conductores por Utilidad")
ranking = df_filtrado.groupby("Conductor")["Utilidad"].sum().sort_values(ascending=False)
st.dataframe(ranking, use_container_width=True)


# =====================================
# DIAGNÓSTICO INTELIGENTE OPERATIVO
# =====================================

st.subheader("🧠 Diagnóstico Inteligente Operativo")




# =====================================
# 📈 ANÁLISIS TEMPORAL INTELIGENTE
# =====================================

st.subheader("📈 Tendencia Mensual del Negocio")

# Asegurar formato fecha
df_filtrado["Fecha_Envio"] = pd.to_datetime(df_filtrado["Fecha_Envio"], errors="coerce")

# Crear columna Mes
df_filtrado["Mes"] = df_filtrado["Fecha_Envio"].dt.to_period("M")

# Convertir Cumple_SLA a numérico (1 = cumple, 0 = no cumple)
df_filtrado["SLA_Num"] = df_filtrado["Cumple_SLA"].apply(
    lambda x: 1 if str(x).lower() in ["si", "sí", "true", "1"] else 0
)

# Agrupar por mes
resumen_mensual = (
    df_filtrado
    .groupby("Mes")
    .agg({
        "Ingreso": "sum",
        "Utilidad": "sum",
        "SLA_Num": "mean"
    })
    .reset_index()
)

# Convertir periodo a texto
resumen_mensual["Mes"] = resumen_mensual["Mes"].astype(str)

st.markdown("### 📊 Ingresos y Utilidad por Mes")
st.line_chart(resumen_mensual.set_index("Mes")[["Ingreso", "Utilidad"]])

st.markdown("### 🚚 Cumplimiento SLA (%) por Mes")
st.bar_chart(resumen_mensual.set_index("Mes")["SLA_Num"])





# ===============================
# INTELIGENCIA AVANZADA OPERATIVA
# ===============================

margen = (total_utilidad / total_ingreso) * 100

st.markdown("### 📊 Análisis Predictivo")

# 1️⃣ Riesgo financiero
if margen < 30:
    st.error(f"🚨 Riesgo Alto: Margen bajo ({margen:.2f}%). Se recomienda reducir costos urgentemente.")
elif margen < 40:
    st.warning(f"⚠️ Riesgo Moderado: Margen aceptable pero mejorable ({margen:.2f}%).")
else:
    st.success(f"🟢 Rentabilidad sólida ({margen:.2f}%). Negocio estable.")

# 2️⃣ Evaluación SLA avanzada
if porcentaje_sla < 70:
    st.error("🚨 Riesgo crítico en cumplimiento SLA. Puede afectar contratos.")
elif porcentaje_sla < 85:
    st.warning("⚠️ SLA por debajo del estándar recomendado (85%).")
else:
    st.success("🟢 Cumplimiento SLA óptimo.")

# 3️⃣ Score Inteligente General
score_general = (margen * 0.6) + (porcentaje_sla * 0.4)

st.markdown("### 🧠 Score Inteligente del Sistema")

if score_general >= 85:
    st.success(f"🏆 Sistema Excelente | Score: {score_general:.2f}/100")
elif score_general >= 70:
    st.info(f"👍 Sistema Bueno | Score: {score_general:.2f}/100")
elif score_general >= 50:
    st.warning(f"⚠️ Sistema Regular | Score: {score_general:.2f}/100")
else:
    st.error(f"🚨 Sistema en Riesgo | Score: {score_general:.2f}/100")

#=============

ruta_menor = (
    df_filtrado.groupby("Ruta")["Utilidad"]
    .sum()
    .sort_values()
    .index[0]
)

conductor_top = (
    df_filtrado.groupby("Conductor")["Utilidad"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

st.info(f"📌 Ruta con menor rentabilidad detectada: {ruta_menor}")
st.info(f"🏆 Conductor más rentable detectado: {conductor_top}")

if porcentaje_sla < 85:
    st.warning("⚠️ El cumplimiento SLA está por debajo del estándar recomendado (85%). Se recomienda revisión operativa.")
else:
    st.success("✅ El SLA se encuentra dentro de parámetros saludables.")

# ==============================
# EXPORTAR REPORTE EJECUTIVO
# ==============================
import io

st.subheader("💾 Descargar Reporte Ejecutivo")

def convertir_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Operaciones")
        workbook  = writer.book
        worksheet = writer.sheets["Operaciones"]

        # Formato cabecera
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#0F3460',
            'font_color': 'white',
            'border': 1
        })
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # Ajustar ancho de columnas automáticamente
        for i, col in enumerate(df.columns):
            column_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, column_len)

    output.seek(0)
    return output

excel_data = convertir_excel(df_filtrado)

st.download_button(
    label="📥 Descargar Excel",
    data=excel_data,
    file_name="Reporte_Ejecutivo_Logistico.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# ==============================
# ESTILO CORPORATIVO
# ==============================
st.markdown(
    """
    <style>
    .stMetric {text-align: center; font-size: 20px; font-weight:bold;}
    .stAlert {font-size:18px;}
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
# ESTILO DARK MODE CORPORATIVO
# ==============================
st.markdown(
    """
    <style>
    /* Fondo general del dashboard */
    .main {
        background-color: #0D0D0D;
        color: #FFFFFF;
    }

    /* Títulos */
    h1, h2, h3, h4, h5, h6 {
        color: #FFD700;
        font-weight: bold;
    }

    /* KPIs */
    .stMetric {
        background-color: #1A1A2E;
        color: #FFFFFF;
        padding: 20px;
        border-radius: 8px;
        font-size: 22px;
        text-align: center;
    }

    /* Alertas */
    .stAlert {
        font-size:18px;
        font-weight:bold;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: #0F3460;
        color: #FFFFFF;
    }
    .css-1d391kg label {
        color: #FFFFFF;
        font-weight: bold;
    }

    /* Dataframe tabla */
    .stDataFrame table {
        background-color: #1A1A2E;
        color: #FFFFFF;
    }

    /* Botones */
    .stButton button {
        background-color: #E94560;
        color: #FFFFFF;
        font-weight: bold;
        border-radius: 5px;
    }
    .stButton button:hover {
        background-color: #FFD700;
        color: #0D0D0D;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# ======================================================



    #=====================================

st.markdown("---")
st.subheader("📄 Reporte Ejecutivo")

pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                        "..", "reports", "ejecutivo", "Reporte_Ejecutivo_20260303.pdf")

if os.path.exists(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    st.download_button(
        label="📥 Descargar Reporte Ejecutivo PDF",
        data=pdf_bytes,
        file_name="Reporte_Ejecutivo_20260303.pdf",
        mime="application/pdf"
    )
else:
    st.warning("PDF no encontrado")




