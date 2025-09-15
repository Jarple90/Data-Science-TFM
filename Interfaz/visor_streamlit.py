### Para activar el proyecto, siga estas indicaciones y disfrute del programa en el localhost ###
# cd "R:\Data Science TFM\Interfaz"
# python -m streamlit run visor_streamlit.py

### Importamos librería ###

import streamlit as st  # para crear la interfaz web interactiva del dashboard
import pandas as pd  # para manipulación y análisis de datos tabulares
import os # para operaciones con rutas, archivos y carpetas del sistema
import importlib.util # para cargar módulos dinámicamente desde rutas especicifas 
import plotly.express as px # para generar gráficos interactivos y visualizaciones avanzadas

from PIL import Image  # para cargar y mostrar imágenes (por ejemplo, logos)

# Configuración general del dashboard: título de la pestaña y diseño ancho
st.set_page_config(page_title="TFM · Presupuestos Generales del Estado", layout="wide")

# Carga del logo institucional desde archivo local
logo_ucm = Image.open("logo_ucm.png")  # Asegúrate de que el archivo esté en la misma carpeta o ruta correcta
st.image(logo_ucm, width=120)          # Muestra el logo con ancho fijo en píxeles

# Encabezado principal del dashboard con estilo HTML personalizado
st.markdown("""
<div style='text-align:center; padding:10px;'>
    <h1 style='color:#00BFFF;'>📊 Presupuestos Generales del Estado</h1>  <!-- Título principal -->
    <h3 style='color:gray;'>TFM · Data Science, Big Data & Business Analytics</h3>  <!-- Subtítulo académico -->
    <p style='font-size:16px;'>Autor: <strong>José Antonio Romero Pérez</strong> · 📍 Málaga · 🗓️ Septiembre 2025</p>  <!-- Datos del autor -->
</div>
""", unsafe_allow_html=True)

# Descripción institucional del proyecto con fondo claro y borde
st.markdown("""
<div style='background-color:#F9F9F9; padding:15px; border-radius:8px; border:1px solid #DDD;'>
    <p style='color:#333333; font-size:16px;'>
    Este dashboard forma parte del Trabajo Fin de Máster en <strong>Data Science, Big Data y Business Analytics</strong>, desarrollado por José Antonio Romero Pérez.  
    Su objetivo es facilitar el análisis comparativo de los <strong>Presupuestos Generales del Estado</strong>, permitiendo a analistas, gestores públicos y auditores explorar, agrupar y visualizar datos presupuestarios de forma intuitiva, escalable y trazable.
    <br><br>
    La herramienta permite cargar presupuestos por año y serie, aplicar filtros dinámicos, realizar agrupaciones por capítulos, programas o códigos económicos, y generar visualizaciones interactivas para evaluar la evolución presupuestaria entre ejercicios.
    <br><br>
    Está construida con <strong>Python, pandas, Streamlit y Plotly</strong>, y diseñada para integrarse fácilmente en entornos institucionales donde la transparencia, la automatización y la auditabilidad son clave.
    </p>
</div>
""", unsafe_allow_html=True)

# Ruta raíz del proyecto
ruta_tfm = r"R:\Data Science TFM"  # Ruta donde se almacenan los presupuestos por año y serie

# Función para cargar archivo
def cargar_archivo(ruta_archivo): # Carga archivos .py (buscando un DataFrame dentro del módulo) o .csv con codificación latina
    df = None
    if ruta_archivo.endswith(".py"):
        try:
            spec = importlib.util.spec_from_file_location("modulo_presupuesto", ruta_archivo)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            for nombre in dir(modulo):
                objeto = getattr(modulo, nombre)
                if isinstance(objeto, pd.DataFrame):
                    df = objeto
                    break
        except Exception as e:
            st.error(f"Error al importar el archivo .py: {e}")
    elif ruta_archivo.endswith(".csv"):
        try:
            df = pd.read_csv(ruta_archivo, encoding="latin1", sep=";")
            df.fillna('', inplace=True)
        except Exception as e:
            st.error(f"Error al leer el archivo CSV: {e}")
    return df

# Limpieza de columnas numéricas 
def limpiar_columnas_numericas(df): # Convierte columnas con nombres como "importe", "total", "euros", etc. a formato numérico estándar
    df_limpio = df.copy()
    for col in df.columns:
        if any(palabra in col.lower() for palabra in ["importe", "total", "euros", "gasto", "presupuesto"]):
            df_limpio[col] = (
                df[col].astype(str)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
                .str.replace("€", "", regex=False)
                .str.replace("%", "", regex=False)
            )
            df_limpio[col] = pd.to_numeric(df_limpio[col], errors="coerce")
    return df_limpio

# 📂 Selección de presupuesto base
st.markdown("## 🧭 Visualización del presupuesto base")
col1, col2 = st.columns(2)
with col1:
    años_disponibles = [d for d in os.listdir(ruta_tfm) if d.startswith("Año")]
    año_base = st.selectbox("📅 Año base", años_disponibles)
with col2:
    serie_base = st.selectbox("📁 Serie", ["Serie Roja", "Serie Verde"])

nivel_base = None
if serie_base == "Serie Verde":
    nivel_base = st.selectbox("🏛️ Nivel institucional", ["ESTADO", "ORGANISMOS AUTÓNOMOS", "RESTO DE ENTIDADES"])

# Navegación por carpetas 
# Permite seleccionar año, serie (Roja o Verde), nivel institucional (si aplica), sección y documento
# Construye la ruta final al archivo presupuestario

if serie_base == "Serie Roja":
    ruta_base = os.path.join(ruta_tfm, año_base, serie_base)
    secciones = [d for d in os.listdir(ruta_base) if os.path.isdir(os.path.join(ruta_base, d))]
    seccion = st.selectbox("🏢 Sección", secciones)
    ruta_seccion = os.path.join(ruta_base, seccion)
    carpetas = [d for d in os.listdir(ruta_seccion) if os.path.isdir(os.path.join(ruta_seccion, d))]
    carpeta = st.selectbox("📄 Documento", carpetas)
    ruta_documento = os.path.join(ruta_seccion, carpeta)
else:
    ruta_base = os.path.join(ruta_tfm, año_base, serie_base, nivel_base)
    carpetas = [d for d in os.listdir(ruta_base) if os.path.isdir(os.path.join(ruta_base, d))]
    carpeta = st.selectbox("📄 Documento", carpetas)
    ruta_documento = os.path.join(ruta_base, carpeta)

# Cargar archivo
# Carga el archivo seleccionado y lo limpia si es válido
# Muestra mensaje de éxito o error según el resultado
archivos = [f for f in os.listdir(ruta_documento) if f.endswith(".csv") or f.endswith(".py")]
if not archivos:
    st.error(f"No hay archivos válidos en {ruta_documento}")
    st.stop()

archivo_base = st.selectbox("📁 Archivo", archivos)
ruta_archivo_base = os.path.join(ruta_documento, archivo_base)
df_base = cargar_archivo(ruta_archivo_base)
df_base = limpiar_columnas_numericas(df_base)

if df_base is not None and not df_base.empty:
    st.markdown("<div style='color:limegreen;font-weight:bold;'>✅ Archivo cargado correctamente</div>", unsafe_allow_html=True)

    columnas_numericas = df_base.select_dtypes(include="number").columns.tolist()
    columnas_categoricas = df_base.select_dtypes(exclude="number").columns.tolist()

    st.markdown("### 📊 Vista previa del presupuesto")
    with st.expander("🔍 Ver tabla completa"):
        st.dataframe(df_base)

    if columnas_numericas and columnas_categoricas:
        st.markdown("### 📋 Agrupación y resumen")
        col_agrupacion = st.selectbox("Agrupar por", columnas_categoricas, key="agrupacion_base")
        col_valor = st.selectbox("Sumar por", columnas_numericas, key="valor_base")

        if col_agrupacion and col_valor:
            df_agrupado = df_base.groupby(col_agrupacion)[col_valor].sum().reset_index()
            st.dataframe(df_agrupado)

            with st.expander("📊 Ver gráfico de barras"):
                fig_bar = px.bar(df_agrupado, x=col_agrupacion, y=col_valor, title=f"{col_valor} por {col_agrupacion}")
                st.plotly_chart(fig_bar, use_container_width=True)

            with st.expander("📈 Ver gráfico de líneas"):
                fig_line = px.line(df_agrupado, x=col_agrupacion, y=col_valor, markers=True)
                st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.markdown("<div style='color:orange;'>⚠️ Este documento no contiene columnas numéricas agrupables.</div>", unsafe_allow_html=True)

    # Guardar en session_state para comparación, y poder comparar los datos bases y el año
    st.session_state["df_base"] = df_base.copy()
    st.session_state["año_base"] = año_base
else:
    st.markdown("<div style='color:red;'>❌ El archivo está vacío o no se pudo cargar correctamente.</div>", unsafe_allow_html=True)
# 📊 Comparación con otro presupuesto, para comparar los distintos años
st.markdown("---")
st.markdown("## 🔄 Comparación entre presupuestos")

# Verifica que el presupuesto base esté cargado, comprobación
if "df_base" not in st.session_state or st.session_state["df_base"] is None:
    st.markdown("<div style='color:orange;'>⚠️ Primero debes cargar un presupuesto base en la sección superior.</div>", unsafe_allow_html=True)
    st.stop()

# Selección del segundo presupuesto
col1, col2 = st.columns(2)
with col1:
    año_comparado = st.selectbox("📅 Segundo año", [a for a in años_disponibles if a != st.session_state["año_base"]])
with col2:
    serie_comparada = st.selectbox("📁 Serie del segundo año", ["Serie Roja", "Serie Verde"], key="serie_comparada")

nivel_comparado = None
if serie_comparada == "Serie Verde":
    nivel_comparado = st.selectbox("🏛️ Nivel institucional", ["ESTADO", "ORGANISMOS AUTÓNOMOS", "RESTO DE ENTIDADES"], key="nivel_comparado")

# Navegación por carpetas del segundo presupuesto
if serie_comparada == "Serie Roja":
    ruta_base = os.path.join(ruta_tfm, año_comparado, serie_comparada)
    secciones = [d for d in os.listdir(ruta_base) if os.path.isdir(os.path.join(ruta_base, d))]
    seccion = st.selectbox("🏢 Sección del segundo año", secciones, key="seccion_comparada")
    ruta_seccion = os.path.join(ruta_base, seccion)
    carpetas = [d for d in os.listdir(ruta_seccion) if os.path.isdir(os.path.join(ruta_seccion, d))]
    carpeta = st.selectbox("📄 Documento", carpetas, key="carpeta_comparada")
    ruta_documento = os.path.join(ruta_seccion, carpeta)
else:
    ruta_base = os.path.join(ruta_tfm, año_comparado, serie_comparada, nivel_comparado)
    carpetas = [d for d in os.listdir(ruta_base) if os.path.isdir(os.path.join(ruta_base, d))]
    carpeta = st.selectbox("📄 Documento", carpetas, key="carpeta_comparada_verde")
    ruta_documento = os.path.join(ruta_base, carpeta)

# Cargar archivo del segundo presupuesto
archivos = [f for f in os.listdir(ruta_documento) if f.endswith(".csv") or f.endswith(".py")]
if not archivos:
    st.markdown("<div style='color:red;'>❌ No hay archivos válidos en la carpeta seleccionada.</div>", unsafe_allow_html=True)
    st.stop()

archivo_comparado = st.selectbox("📁 Archivo del segundo año", archivos, key="archivo_comparado")
ruta_archivo_comparado = os.path.join(ruta_documento, archivo_comparado)
df_comparado = cargar_archivo(ruta_archivo_comparado)
df_comparado = limpiar_columnas_numericas(df_comparado)

if df_comparado is None or df_comparado.empty:
    st.markdown("<div style='color:red;'>❌ El archivo del segundo año está vacío o no se pudo cargar.</div>", unsafe_allow_html=True)
    st.stop()

# Preparar comparación
df_base = st.session_state["df_base"].copy()
df_base["Año"] = st.session_state["año_base"]
df_comparado["Año"] = año_comparado
df_total = pd.concat([df_base, df_comparado], ignore_index=True)

columnas_numericas = df_total.select_dtypes(include="number").columns.tolist()
columnas_categoricas = df_total.select_dtypes(exclude="number").columns.tolist()

st.markdown("### 📊 Vista previa combinada")
with st.expander("🔍 Ver tabla comparativa"):
    st.dataframe(df_total)

if columnas_numericas and columnas_categoricas:
    st.markdown("### 📋 Comparación agrupada")
    col_agrupacion = st.selectbox("Agrupar por", [c for c in columnas_categoricas if c != "Año"], key="agrupacion_comparada")
    col_valor = st.selectbox("Sumar por", columnas_numericas, key="valor_comparada")

    if col_agrupacion and col_valor:
        df_agrupado = df_total.groupby(["Año", col_agrupacion])[col_valor].sum().reset_index()
        st.dataframe(df_agrupado)

        with st.expander("📊 Ver gráfico comparativo"):
            fig = px.bar(df_agrupado, x=col_agrupacion, y=col_valor, color="Año", barmode="group",
                        title=f"{col_valor} por {col_agrupacion} en cada año")
            st.plotly_chart(fig, use_container_width=True)

        with st.expander("📈 Ver evolución por año"):
            fig_line = px.line(df_agrupado, x=col_agrupacion, y=col_valor, color="Año", markers=True)
            st.plotly_chart(fig_line, use_container_width=True)
else:
    st.markdown("<div style='color:orange;'>⚠️ Los archivos no contienen columnas numéricas agrupables.</div>", unsafe_allow_html=True)

# 🔮 Predicción presupuestaria
st.markdown("---")
st.markdown("## 🔮 Predicción presupuestaria")

st.markdown("""
<div style='background-color:#F0F8FF; padding:10px; border-radius:6px; border:1px solid #CCC;'>
<p style='color:#333333; font-size:15px;'>
Esta sección permite estimar el comportamiento presupuestario en ejercicios futuros mediante un modelo de regresión lineal.  
Selecciona una variable numérica y el visor proyectará su evolución para los próximos años.
</p>
</div>
""", unsafe_allow_html=True)

from sklearn.linear_model import LinearRegression
import numpy as np

with st.expander("📈 Mostrar módulo de predicción"):
    if df_total is None or df_total.empty:
        st.warning("⚠️ Primero debes cargar y comparar los presupuestos.")
        st.stop()

    columnas_numericas = df_total.select_dtypes(include="number").columns.tolist()
    col_prediccion = st.selectbox("📌 Variable a predecir", columnas_numericas, key="col_prediccion")

    # Agrupación por año y limpieza de la columna "Año"
    df_modelo = df_total[["Año", col_prediccion]].dropna().copy()
    df_modelo["Año"] = df_modelo["Año"].astype(str).str.extract(r'(\d{4})').astype(int)

    # Entrenamiento del modelo
    X = df_modelo[["Año"]]
    y = df_modelo[col_prediccion]

    modelo = LinearRegression()
    modelo.fit(X, y)

    # Predicción para años futuros
    años_futuros = st.slider("📅 Años a predecir", min_value=1, max_value=5, value=3)
    ultimo_año = df_modelo["Año"].max()
    años_pred = pd.DataFrame({"Año": [ultimo_año + i for i in range(1, años_futuros + 1)]})
    predicciones = modelo.predict(años_pred)

    # Mostrar resultados
    df_pred = años_pred.copy()
    df_pred[col_prediccion] = predicciones

    st.markdown("### 📊 Resultados de la predicción")
    st.dataframe(df_pred)

    # Visualización conjunta
    df_vis = pd.concat([df_modelo, df_pred], ignore_index=True)
    df_vis["Origen"] = ["Histórico"] * len(df_modelo) + ["Predicción"] * len(df_pred)

    fig_pred = px.line(df_vis, x="Año", y=col_prediccion, color="Origen", markers=True,
                    title=f"Predicción de {col_prediccion} para años futuros")
    st.plotly_chart(fig_pred, use_container_width=True)


# Pie de página
st.markdown("---")
st.markdown(
    "<div style='text-align: right; font-size:14px;'>🧑‍💻 <strong>José Antonio Romero Pérez</strong> · TFM · Data Science · 📍 Málaga</div>",
    unsafe_allow_html=True
)




